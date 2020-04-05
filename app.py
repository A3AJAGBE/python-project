#To import Flask library
from flask import Flask, render_template, request, redirect, url_for, session

#To secure the password in the database
import hashlib

#To connect to the database
import mysql.connector

app = Flask(__name__)
app.secret_key = 'My SecretKEY'

#connection information to the database
config = {
  'user': 'root',
  'password': 'root',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'raise_on_warnings': True,
  'database': 'DrugSystem'
}

link = mysql.connector.connect(**config)

#This is to display the users home page of the website.
@app.route('/')
def home():
    return render_template('index.html')

#This is to display the dashboard page of the website.
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # verify if the Administrator is logged in
    if 'loggedin' in session:
        # redirect Administrator to dashboard
        return render_template('dashboard.html', username=session['username'])
    # if not redirect to the login page
    return redirect(url_for('admin_main'))


#This is to display the admin home/login page of the website
@app.route('/admin_main', methods=['GET', 'POST'])
def admin_main():

    output = ' '
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(str(request.form['password']).encode('utf-8')).hexdigest()

        #mysql query
        mycursor = link.cursor()
        mycursor.execute('SELECT username, password FROM Administrators WHERE username = %s AND password = %s', (username, password))
        usernameCheck = mycursor.fetchone()

        # check if username and password in the database
        if usernameCheck:
            # Create session data
            session['loggedin'] = True
            # session['id'] = Administrators['A_Id']
            session['username'] = username

            # Redirect to dashboard page
            return redirect(url_for('dashboard'))
        else:
            # Administrator doesnt exist or username/password is incorrect
            output = 'Incorrect login information, Try again'
    return render_template('admin_main.html', output = output)

#This is to display the contact page of the website to new Administrator requesting for access
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    output = ' '
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']

        #mysql query
        mycursor = link.cursor()
        mycursor.execute('SELECT username,email FROM LoginAccess WHERE username = %s or email = %s', (username, email))
        usernameCheck = mycursor.fetchone()

        if usernameCheck:
            output = 'Account already exist for this email or username!!!'
        else:
            mycursor.execute("INSERT INTO LoginAccess (Name, Username, Email) VALUES (%s, %s, %s)", (name, username, email) )
            link.commit()
            output = 'Request sent successfully and email will be sent soon'
    return render_template('contact.html', output = output)

""" This is to display the admin register page of the website """
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    output = ' '
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = hashlib.sha256(str(request.form['password']).encode('utf-8')).hexdigest()
        con_password = hashlib.sha256(str(request.form['con_password']).encode('utf-8')).hexdigest()

        #mysql query
        mycursor = link.cursor()
        mycursor.execute('SELECT username FROM Administrators WHERE username = %s', (username,))
        usernameCheck = mycursor.fetchone()

        if usernameCheck:
            output = 'Account already exists!'
        else:
            mycursor.execute('INSERT INTO Administrators (Name, Username, Password, confirmPassword) VALUES (%s, %s, %s, %s)', (name, username, password, con_password) )
            link.commit()
            output = 'Administrator successfully created'
    return render_template('admin_register.html', output = output)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('admin_main'))

if __name__ == '__main__':
    app.run()
