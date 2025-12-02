"""
Simple Flask Application with intentional vulnerabilities for SAST testing
"""
from flask import Flask, request, render_template_string
import subprocess
import sqlite3
import os

app = Flask(__name__)

# Database setup
def get_db():
    conn = sqlite3.connect('users.db')
    return conn

@app.route('/')
def home():
    return "Welcome to the SAST Demo App!"

# Vulnerability 1: SQL Injection
@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    conn = get_db()
    cursor = conn.cursor()
    # Vulnerable: SQL Injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    return str(result)

# Vulnerability 2: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host')
    # Vulnerable: Command Injection
    result = subprocess.os.popen(f"ping -c 1 {host}").read()
    return result

# Vulnerability 3: XSS (Cross-Site Scripting)
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    # Vulnerable: XSS via template injection
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)

# Vulnerability 4: Hardcoded Secret
API_KEY = "sk-secret-api-key-12345"
DATABASE_PASSWORD = "admin123"

@app.route('/config')
def config():
    return f"API configured with key: {API_KEY[:5]}..."

# Vulnerability 5: Insecure Deserialization hint
import pickle

@app.route('/load')
def load_data():
    data = request.args.get('data')
    if data:
        # Vulnerable: Insecure deserialization
        obj = pickle.loads(bytes.fromhex(data))
        return str(obj)
    return "No data"

if __name__ == '__main__':
    # Vulnerability 6: Debug mode enabled in production
    app.run(debug=True, host='0.0.0.0')
