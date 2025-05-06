from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess

app = Flask(__name__)
app.secret_key = '1'

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="nutribot"
)
cursor = conn.cursor(dictionary=True)

# ---------- Routes ---------- #

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO users (username, email, password, is_admin) VALUES (%s, %s, %s, 0)",
                           (username, email, hashed_password))
            conn.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return render_template('register.html', message="⚠️ Error: " + str(err))
    return render_template('register.html', message='')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('nutribot'))
        else:
            return render_template('login.html', message="❌ Invalid username or password")
    return render_template('login.html', message='')

import os

@app.route('/nutribot')
def nutribot():
    if 'username' not in session:
        return redirect(url_for('login'))

    nutribot_script = os.path.join(os.path.dirname(__file__), "nutribot_gradio.py")
    subprocess.Popen(["python", nutribot_script])
    return f"<h2>✅ Hello {session['username']}! Nutribot is launching...</h2><p>Gradio app is now available on <a href='http://localhost:7860' target='_blank'>localhost:7860</a></p>"

# ---------- Run Server ---------- #
if __name__ == '__main__':
    app.run(debug=True)