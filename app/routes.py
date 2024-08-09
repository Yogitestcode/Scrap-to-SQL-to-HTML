from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from users.forms import LoginForm, RegistrationForm
from users.models import User
from app.db import pool
import mysql.connector

main = Blueprint('main', __name__)




@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    search_query = request.form.get('search_query', '')
    books = []

    try:
        with pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                if search_query:
                    query = "SELECT * FROM books WHERE title LIKE %s"
                    cursor.execute(query, (f"%{search_query}%",))
                else:
                    cursor.execute("SELECT * FROM books")
                books = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        books = []
    return render_template('index.html', books=books, search_query=search_query)

@main.route('/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
                conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return redirect(url_for('main.index'))

@main.route('/add', methods=['POST'])
@login_required
def add_book():
    title = request.form['title']
    price = request.form['price']
    availability = request.form['availability']
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO books (title, price, availability) VALUES (%s, %s, %s)", (title, price, availability))
                conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return redirect(url_for('main.index'))

@main.route('/update', methods=['POST'])
@login_required
def update_book():
    book_id = request.form['id']
    new_title = request.form['title']
    new_price = request.form['price']
    new_availability = request.form['availability']
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE books SET title = %s, price = %s, availability = %s WHERE id = %s", (new_title, new_price, new_availability, book_id))
                conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return redirect(url_for('main.index'))
