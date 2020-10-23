import MySQLdb.cursors
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'hotdog'

app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-01.cleardb.net'
app.config['MYSQL_USER'] = 'b2c04ab25f2fad'
app.config['MYSQL_PASSWORD'] = 'e2f37027'
app.config['MYSQL_DB'] = 'heroku_4f71138a5925978'

# Initialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests


@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee_accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in our database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['name'] = account['name']
            session['username'] = account['username']
            session['password'] = account['password']
            session['is_manager'] = account['is_manager']
            if session['is_manager'] == 1:
                # Redirect to manager home page
                return render_template('manager_home.html', account=account)
            else:
                if session['is_manager'] == 0:
                    # Redirect to employee home page
                    return render_template('employee_home.html', account=account)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/insert')
def insert():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('insert.html')
    else:
        return redirect(url_for('login'))


@app.route('/insert_account')
def insert_account():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('insert.account.html')
    else:
        return redirect(url_for('login'))


@app.route('/timestamp')
def timestamp():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('timestamp.html')
    else:
        return redirect(url_for('login'))


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['is_manager'] == 1:
            return redirect(url_for('manager_home'))
        else:
            if session['is_manager'] == 0:
                return redirect(url_for('employee_home'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/employee_home')
def employee_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('employee_home.html', account=session)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/manager_home')
def manager_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('manager_home.html', account=session)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee_accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/reports')
def reports():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee_accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        if account['is_manager'] == 1:
            # Show the manager profile page with account info
            return redirect(url_for('manager_reports'))
        else:
            if session['is_manager'] == 0:
                # Show the employee profile page with account info
                return redirect(url_for('employee_reports'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/employee_reports')
def employee_reports():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM assigned WHERE id = %s', (session['id'],))
        assigned = cursor.fetchone()
        # User is loggedin show them the home page
        return render_template('employee_reports.html', assigned=assigned)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/manager_reports')
def manager_reports():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the report page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee_accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('manager_reports.html', account=session)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/assignments')
def assignments():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee_accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('assignments.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/tasks')
def tasks():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee_accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('tasks.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/projects')
def projects():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee_accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('projects.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
