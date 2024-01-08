#!/usr/bin/env python3

from flask import Flask, redirect, render_template, request, url_for
import flask_login

app = Flask(__name__)
app.secret_key = "J7pL#uQX2G4sP9nH6eR0kZ8mF3aD1wY5vO2oL4iE7cT9"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'seb': {'password': 'secret'}, 'hackerman': {'password': 'hackersarehere'}}
user = None

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def load_user(username):
    if username not in users: 
        return None
    user = User()
    user.id = username
    return user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    global user
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username not in users:
            return redirect('/login')
        if password != users[username]['password']:
            return redirect('/login')
        
        user = load_user(username)
        flask_login.login_user(user)
        return redirect('/authenticated')
    else:
        return render_template('login.html')

@app.route('/authenticated')
@flask_login.login_required
def loggedin():
    return render_template('welcome.html', user=user.id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
