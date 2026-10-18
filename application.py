from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from user import User
import db_manager
from os import getenv
import os

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY_SESSION')

@app.route('/')
def index():
    if 'email' in session:
        user = User.get_user_by_email(session['email'])
        return redirect(url_for('home'))
    if db_manager.conta_utenti() == 0:
        return redirect(url_for('register_admin'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        return render_template('index.html',utente=utente)
    return redirect('login')

@app.route('/register_admin', methods=['POST', 'GET'])
def register_admin():
    if request.method == 'POST' and db_manager.conta_utenti() == 0:
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        print(f"Name: {name}, Surname: {surname}")  # Debugging line
        print(f"Email: {email}, Password: {password}")  # Debugging line
        if password != confirm_password:
            flash("Errore 400: Le password non coincidono", "error")
            return redirect(url_for('register_admin'))
        user = User(name, surname, email, password)
        user.create_user()
        return redirect(url_for('login'))
    elif db_manager.conta_utenti()!=0:
        return redirect(url_for('login'))
    return render_template('register_admin.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Email: {email}, Password: {password}")  # Debugging line
        user = User.get_user_by_email(email)
        if user == None:
            flash("Errore 401: Email e/o password non valide", "error")
            return redirect(url_for('login'))
        if user.check_password(password):
            session['email'] = email
            return redirect(url_for('home'))
        flash("Errore 401: Email e/o password non valide", "error")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__== '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)