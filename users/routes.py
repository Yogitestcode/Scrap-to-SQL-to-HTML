from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from users.forms import LoginForm, RegistrationForm
from users.models import User
from app.db import pool
import mysql.connector

users_bp = Blueprint('users', __name__, )

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
   
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #to connect into sql and confirm username password
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            # Assuming login_user function logs in the user and User is a user model
            login_user(User(user['id'], user['username'], user['password']))
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('users_bp.login'))

    return render_template('login.html')
    

@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            connection = pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            cursor.close()
            connection.close()
            flash('Registration successful', 'success')
            return redirect(url_for('users.login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
    return render_template('register.html', form=form)