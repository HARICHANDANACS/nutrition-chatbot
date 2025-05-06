import pickle
import pandas as pd
import requests
import gradio as gr
from transformers import pipeline

# Load trained model for diet recommendation
with open("meal_recommendation_model.pkl", "rb") as file:
    loaded_model = pickle.load(file)

# Load dataset
file_path = "input.csv"
df = pd.read_csv(file_path)
df['VegNovVeg'] = df['VegNovVeg'].astype('category').cat.codes

# Hugging Face pipeline for NLP
nlp = pipeline('question-answering')

# Nutrition API key
API_KEY = '50rflTDxjhA6bO38r1pV2w==DBgJkhj1jlHOYVTs'

def recommend_foods(calories, veg_only=True, high_protein=False, low_carb=False):
    min_cal = calories * 0.75
    max_cal = calories * 1.25

    filtered_df = df[(df['Calories'] >= min_cal) & (df['Calories'] <= max_cal)].copy()

    if veg_only:
        filtered_df = filtered_df[filtered_df['VegNovVeg'] == 0]
    if high_protein:
        filtered_df = filtered_df[filtered_df['Proteins'] >= 8]
    if low_carb:
        filtered_df = filtered_df[filtered_df['Carbohydrates'] <= 40]

    if filtered_df.empty:
        filtered_df = df[(df['Calories'] >= min_cal) & (df['Calories'] <= max_cal)].copy()
    if filtered_df.empty:
        return "❌ No suitable foods found."

    X_filtered = filtered_df[['Calories', 'Fats', 'Proteins', 'Iron', 'Calcium', 'Sodium', 
                              'Potassium', 'Carbohydrates', 'Fibre', 'VitaminD', 'Sugars', 'VegNovVeg']]

    predictions = loaded_model.predict(X_filtered)

    filtered_df.loc[:, 'Breakfast'] = predictions[:, 0]
    filtered_df.loc[:, 'Lunch'] = predictions[:, 1]
    filtered_df.loc[:, 'Dinner'] = predictions[:, 2]

    breakfast_foods = filtered_df.loc[filtered_df['Breakfast'] == 1, 'Food_items'].tolist()
    lunch_foods = filtered_df.loc[filtered_df['Lunch'] == 1, 'Food_items'].tolist()
    dinner_foods = filtered_df.loc[filtered_df['Dinner'] == 1, 'Food_items'].tolist()

    if not breakfast_foods:
        breakfast_foods = filtered_df['Food_items'].sample(1).tolist()
    if not lunch_foods:
        lunch_foods = filtered_df['Food_items'].sample(1).tolist()
    if not dinner_foods:
        dinner_foods = filtered_df['Food_items'].sample(1).tolist()

    diet_plan = {
        "Breakfast": breakfast_foods,
        "Lunch": lunch_foods,
        "Dinner": dinner_foods
    }

    result = f"\U0001F37D️ Recommended Diet Plan for {calories} Calories:\n"
    for meal, foods in diet_plan.items():
        result += f"{meal}: {', '.join(foods)}\n"
    return result

def get_food_nutrition(food_name):
    api_url = 'https://api.api-ninjas.com/v1/nutrition'
    params = {'query': food_name}
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def calculate_bmi(weight, height):
    height_meters = height / 100
    return round(weight / (height_meters ** 2), 2)

def calculate_calories_to_lose_weight(desired_weight_loss_kg):
    return desired_weight_loss_kg * 7700

def calculate_bmr(weight, height, age, gender, equation='mifflin_st_jeor'):
    if equation == 'mifflin_st_jeor':
        if gender == 'male':
            return 10 * weight + 6.25 * height - 5 * age + 5
        else:
            return 10 * weight + 6.25 * height - 5 * age - 161
    elif equation == 'harris_benedict':
        if gender == 'male':
            return 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age
        else:
            return 447.593 + 9.247 * weight + 3.098 * height - 4.33 * age

def calculate_tdee(bmr, activity_level):
    activity_factors = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'super_active': 1.9
    }
    return bmr * activity_factors.get(activity_level, 1)

def calculate_ibw(height, gender):
    if gender == 'male':
        return 50 + 2.3 * max(0, height - 60)
    elif gender == 'female':
        return 45.5 + 2.3 * max(0, height - 60)
    else:
        return None

def chatbot(user_input, weight, height, age, gender, activity_level, desired_weight_loss_kg, food_name):
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    ibw = calculate_ibw(height, gender)
    calories_to_lose_weight = calculate_calories_to_lose_weight(desired_weight_loss_kg)
    nutrients = get_food_nutrition(food_name)

    response = f"\n\U0001F4DD Health Calculations:\nBMI: {bmi}\nBMR: {bmr}\nTDEE: {tdee}\nIBW: {ibw}\nCalories to lose {desired_weight_loss_kg} kg: {calories_to_lose_weight} kcal\n"

    if nutrients:
        response += "\n\U0001F4CA Nutritional Information:\n"
        for item in nutrients:
            response += f"Food: {item.get('name', '-')}, Calories: {item.get('calories', '-')}, Protein: {item.get('protein', '-')}g, Carbs: {item.get('carbohydrates', '-')}g, Fat: {item.get('fat', '-')}g\n"
    else:
        response += "\nNo nutritional data found for the given food.\n"

    context = "The bot provides nutrition info like calories, protein, carbs, fat."
    answer = nlp(question=user_input, context=context)
    response += f"\nBot Answer: {answer['answer']}"
    return response

# Diet Plan Tab
diet_interface = gr.Interface(
    fn=recommend_foods,
    inputs=[
        gr.Slider(minimum=100, maximum=1000, step=50, value=500, label="Calories"),
        gr.Checkbox(label="Vegetarian Only", value=True),
        gr.Checkbox(label="High Protein", value=False),
        gr.Checkbox(label="Low Carb", value=False)
    ],
    outputs="text",
    title="Personalized Diet Plan"
)

# Health Chatbot Tab
chatbot_interface = gr.Interface(
    fn=chatbot,
    inputs=[
        gr.Textbox(label="Ask the Bot (e.g., What is a good protein intake?)"),  # user_input
        gr.Number(label="Weight (kg)"),                                           # weight
        gr.Number(label="Height (cm)"),                                           # height
        gr.Number(label="Age (years)"),                                           # age
        gr.Radio(["male", "female"], label="Gender"),                             # gender
        gr.Radio(["sedentary", "lightly_active", "moderately_active", "very_active", "super_active"], label="Activity Level"),  # activity_level
        gr.Number(label="Desired Weight Loss (kg)"),                              # desired_weight_loss_kg
        gr.Textbox(label="Food Name (e.g., banana, rice, chicken)")               # food_name
    ],
    outputs="text",
    title="Health and Nutrition Chatbot"
)

# Launch app with tabs
gr.TabbedInterface([diet_interface, chatbot_interface], ["Diet Plan", "Health Bot"]).launch()
