from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

USER_DATA_FILE = 'user_data.json'
ADMIN_PASSWORD = "#Switch2021"  # Change this to a secure password

def store_user_data(username, password):
    user_data = {username: password}
    
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            existing_data = json.load(f)
        existing_data.update(user_data)
    else:
        existing_data = user_data

    with open(USER_DATA_FILE, 'w') as f:
        json.dump(existing_data, f)

def access_user_data(admin_password):
    if admin_password != ADMIN_PASSWORD:
        return None

    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        store_user_data(username, password)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/access', methods=['GET', 'POST'])
def access():
    if request.method == 'POST':
        admin_password = request.form['admin_password']
        user_data = access_user_data(admin_password)
        if user_data is not None:
            return render_template('access.html', user_data=user_data)
        return "Access Denied: Incorrect Admin Password"
    return render_template('access.html', user_data={})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
