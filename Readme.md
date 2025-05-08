# 🥗 Nutribot – AI-powered Health & Diet Recommendation System

Nutribot is an intelligent nutrition assistant that helps users generate personalized diet plans and get insights into their health metrics. It uses machine learning for meal recommendations, a chatbot for health calculations, and integrates nutrition data from an external API. The app is built using Python, Gradio, Flask, and MySQL.

---

## 🚀 Features

- 🔐 User authentication with Flask & MySQL
- 🧠 ML-based meal recommendation system
- 🍱 Personalized diet plans based on calories and preferences
- 💬 Health chatbot to calculate:
  - BMI (Body Mass Index)
  - BMR (Basal Metabolic Rate)
  - TDEE (Total Daily Energy Expenditure)
  - IBW (Ideal Body Weight)
  - Calories needed to lose weight
- 🥦 Nutrition analysis using [API Ninjas Nutrition API](https://api-ninjas.com/api/nutrition)
- 🎛️ Easy-to-use Gradio interface with two tabs:
  - **Health Bot**
  - **Diet Plan**

---

## 📁 Project Structure

```
nutribot/
├── app.py                     # Flask login system and Gradio launcher
├── nutribot_gradio.py         # Main Gradio app
├── meal_recommendation_model.pkl  # Trained ML model for meals
├── input.csv                  # Nutrition dataset
├── templates/
│   ├── login.html             # HTML form for login
│   └── register.html          # HTML form for registration
```

---

## 🛠️ Requirements

- Python 3.8 or higher
- MySQL Server
- API Key from [API Ninjas](https://api-ninjas.com/api/nutrition)

---

## 🔧 MySQL Setup

Create the database and user table:

```sql
CREATE DATABASE nutribot;
USE nutribot;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT 0
);
```

---

## 🔑 API Key Configuration

In `nutribot_gradio.py`, replace this line with your API key:

```python
API_KEY = 'your_api_key_here'
```

You can get your free key from: https://api-ninjas.com/api/nutrition

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/nutribot.git
cd nutribot
pip install -r requirements.txt
```

If `requirements.txt` is not available, run:

```bash
pip install gradio pandas requests transformers scikit-learn flask mysql-connector-python
```

---

## ▶️ Running the App

### Option 1: Launch Gradio directly

```bash
python nutribot_gradio.py
```

Visit: [http://localhost:7860](http://localhost:7860)

---

### Option 2: Use Flask with Login System

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

After login or registration, it will redirect and launch the Gradio interface at [http://localhost:7860](http://localhost:7860)

---

## ✨ Usage Guide

### 🔷 Diet Plan Tab
- Enter your daily calorie goal
- Choose filters like vegetarian, high-protein, low-carb
- Get meal suggestions for breakfast, lunch, and dinner

### 🔶 Health Bot Tab
- Ask health-related questions (optional)
- Input height, weight, age, gender, activity level, and a food name
- Get BMI, BMR, TDEE, IBW, and food nutrition facts

---

## 🧪 Demo Login Credentials

For testing the Flask login:

- **Username**: testuser  
- **Email**: test@example.com  
- **Password**: test123

Or you can register a new account.

---



---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## ❤️ Contributions

Feel free to fork this repo, raise issues, or submit pull requests to improve Nutribot!
