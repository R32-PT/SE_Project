import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key = 'hotdog'

app.config['MYSQL_HOST'] = 'sh4ob67ph9l80v61.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'nj317ziyvdn663sh'
app.config['MYSQL_PASSWORD'] = 'd4mj8hlti6ajkw5r'
app.config['MYSQL_DB'] = 'r2e87bd791lbllyo'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    
    message = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        user = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (user, password,))
        loggedIn = cursor.fetchone()

        if loggedIn:
            session['loggedin'] = True
            session['id'] = loggedIn['id']
            session['username'] = loggedIn['username']
            session['password'] = loggedIn['password']
            session['role'] = loggedIn['role']
            mysql.connection.commit()

            if session['role'] == 'ADMIN':
                return render_template("support.html", loggedIn = loggedIn)
            elif session['role'] == 'FINANCE_ADMIN':
                return render_template("finance.html", loggedIn = loggedIn)
            elif session['role'] == 'HR_ADMIN':
                return render_template("hr.html", loggedIn = loggedIn)
            elif session['role'] == 'SALES_ADMIN':
                return render_template("sales.html", loggedIn = loggedIn)
            elif session['role'] == 'TECH_ADMIN':
                return render_template("technology.html", loggedIn = loggedIn)
        
        else:
            message = "log in failed"

    return render_template("login.html",message = message)


@app.route('/support')
def support():
    if 'loggedin' in session:
        return render_template("support.html")
    return redirect(url_for('login'))

@app.route('/finance')
def finance():
    if 'loggedin' in session:
        return render_template("finance.html")
    return redirect(url_for('login'))

@app.route('/sales')
def sales():
    if 'loggedin' in session:
        return render_template("sales.html")
    return redirect(url_for('login'))    

@app.route('/hr')
def hr():
    if 'loggedin' in session:
        return render_template("hr.html")
    return redirect(url_for('login'))

@app.route('/technology')
def technology():
    if 'loggedin' in session:
        return render_template("technology.html")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    session.pop('password',None)
    session.pop('role',None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)