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

def getLinks(roles):
    links = []
    for x in roles:
        if x == 'ADMIN':
            links.extend(["Manage User Accounts","Assign Roles","Help Desk"])
        if x == 'FINANCE_ADMIN':
            links.extend(["Finance Reports", "Accounts Payable","Accounts Receivable","Tax"])
        if x == 'SALES_ADMIN':
            links.extend(["Sales Reports","Sales Leads","Sales Demo"])
        if x == 'HR_ADMIN':
            links.extend(["New Hire On-boarding","Benefits","Payroll","Off-boarding","Hr Reports"])
        if x == 'TECH_ADMIN':
            links.extend(["Application Monitoring","Tech Support","App Development","App Admin","Release Management"])
    
    return links



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
            session['roles'] = loggedIn['roles']
            
            mysql.connection.commit()
            x = session['roles'].split(',')
            p = '  '.join(x)
            y = getLinks(x)

            return render_template("portal.html", loggedIn = loggedIn, p = p, roles = y)
        
        else:
            message = "log in failed, Please try again"

    return render_template("login.html",message = message)


@app.route('/portal')
def support():
    if 'loggedin' in session:
        return render_template("portal.html")
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    session.pop('password',None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)