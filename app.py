from flask import Flask, render_template, request, session, flash, redirect
from flask_mysqldb import MySQL
import pandas as pd

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chatbotx'
mysql = MySQL(app)

# Set a secret key for session management
app.secret_key = '8848'

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        # Verify the email and password in the database
        cur.execute("SELECT * FROM user_info WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        if user:
             # Store the user in the session
            session['email'] = user[1]

            # Show pop-up message
            flash('Logged in successfully!', 'success')

            # Redirect to the search page
            return render_template('search.html')
        else:
            error_message = 'Invalid email or password'
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
       

        cur = mysql.connection.cursor()

        # Check if the email already exists in the database
        cur.execute("SELECT * FROM user_info WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            error_message = 'email already exists'
            return render_template('signup.html', error_message=error_message)

        # Insert the new user data into the database
        cur.execute("INSERT INTO user_info (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()

        # Store the user in the session
        session['email'] = email

        return render_template('login.html')

    return render_template('signup.html')
app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['query']

        cur = mysql.connection.cursor()

        # Perform the search query in the database
        cur.execute("SELECT * FROM search_table WHERE column_name LIKE %s", (f'%{search_query}%',))
        search_results = cur.fetchall()

        # Render the search results template
        return render_template('search_results.html', results=search_results)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
