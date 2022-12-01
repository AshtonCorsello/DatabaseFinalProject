from flask import Flask, request, render_template, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'acorsell'
app.config['MYSQL_PASSWORD'] = '7gbtS0bS'
app.config['MYSQL_DB'] = 'acorsell'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def login() :
    message = ''
    if request.method == 'POST' :
        if request.form['submitButton'] == 'login' :
            password = request.form['password']
            email = request.form['email']
            if email and password :
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM CUSTOMER WHERE Username = %s', (email,))
                account = cursor.fetchone()
                if account :
                    session['LoggedIn'] = True
                    session['ID'] = account['ID']
                    session['username'] = account['Username']
                    session['name'] = account['First_Name']
                    return redirect(url_for('homepage'))
                if not account : 
                    message = "INVALID USERNAME OR PASSWORD" 
        if request.form['submitButton'] == 'register' : 
            return redirect(url_for('register'))
            
    return render_template('index.html', data = message)

@app.route('/register/', methods=['POST', 'GET'])
def register() : 
    requiredField = "* REQUIRED FIELD"
    if request.method == 'POST' : 
        firstName = request.form['firstname']
        lastName = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        streetName = request.form['streetname']
        streetNumber = request.form['streetnumber']
        zipcode = request.form['zipcode']
        zipcode = int(zipcode)
        city = request.form['city']
        state = request.form['state']
        phoneNumber = request.form['phonenumber']
        email = request.form['email']

        if not firstName : 
            return render_template('register.html', requiredFieldFN = requiredField)
        if not lastName :
            return render_template('register.html', requiredFieldLN = requiredField)
        if not username :
            return render_template('register.html', requiredFieldUN = requiredField)
        if not password : 
            return render_template('register.html', requiredFieldPW = requiredField)
        if not streetName : 
            return render_template('register.html', requiredFieldSN = requiredField)
        if not streetNumber : 
            return render_template('register.html', requiredFieldSNU = requiredField)
        if not zipcode : 
            return render_template('register.html', requiredFieldZC = requiredField)
        if not city : 
            return render_template('register.html', requiredFieldCY = requiredField)
        if not state : 
            return render_template('register.html', requiredFieldST = requiredField)
        if not phoneNumber : 
            return render_template('register.html', requiredFieldPN = requiredField)
        if not email : 
            return render_template('register.html', requiredFieldEM = requiredField)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO CUSTOMER (First_Name, Last_Name, Phone_Number, Street, Street_Num, City, State, Zip, Apt, Username, Password, email) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (firstName, lastName, phoneNumber, streetName, streetNumber, city, state, zipcode, 0, username, password, email,))
        mysql.connection.commit()
        return redirect(url_for('login'))


    return render_template('register.html')
    
@app.route('/homepage/', methods=['POST', 'GET'])
def homepage() : 
    loggedIn = session['LoggedIn']
    if loggedIn : 
        return render_template('homepage.html', name = session['name'])
    else : 
        return redirect(url_for('/')) 
    


app.run(host='localhost', port=5002, debug=True)