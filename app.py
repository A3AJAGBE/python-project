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


""" This is the start of User route """
#This is to display the users home page of the website.
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


""" This is the start of Administrator route """
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

#This is to display the admin register page of the website
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if 'loggedin' in session:
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
        return render_template('admin_register.html', output = output, username=session['username'])
    return redirect(url_for('admin_main'))

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('admin_main'))


""" This is the start of Pharma route  """
@app.route('/pharma_login', methods=['GET', 'POST'])
def pharma_login():

    output = ' '
    if request.method == 'POST':
        name = request.form['name']
        password = hashlib.sha256(str(request.form['password']).encode('utf-8')).hexdigest()

        #mysql query
        mycursor = link.cursor()
        mycursor.execute('SELECT name, password FROM Pharmaceuticals WHERE name = %s AND password = %s', (name, password))
        nameCheck = mycursor.fetchone()

        # check if company name and password is in the database
        if nameCheck:
            # Create session data
            session['loggedin'] = True
            session['name'] = name

            # Redirect to dashboard page
            return redirect(url_for('pharma_dashboard'))
        else:
            # Administrator doesnt exist or username/password is incorrect
            output = 'Incorrect login information, Try again'
    return render_template('pharma_login.html', output = output)


@app.route('/pharma_reg', methods=['GET', 'POST'])
def pharma_reg():

    output = ' '
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        password = hashlib.sha256(str(request.form['password']).encode('utf-8')).hexdigest()
        con_password = hashlib.sha256(str(request.form['con_password']).encode('utf-8')).hexdigest()

        #mysql query
        mycursor = link.cursor()
        mycursor.execute('SELECT name FROM Pharmaceuticals WHERE name = %s', (name,))
        nameCheck = mycursor.fetchone()

        if nameCheck:
            output = 'Account already exists!'
        else:
            mycursor.execute('INSERT INTO Pharmaceuticals (Name, Location, Password, confirmPassword) VALUES (%s, %s, %s, %s)', (name, location, password, con_password) )
            link.commit()
            output = 'Account successfully created, Go back login page'
    return render_template('pharma_reg.html', output = output)

@app.route('/pharma_dashboard', methods=['GET', 'POST'])
def pharma_dashboard():
    # verify if the Pharmaceutical Company is logged in
    if 'loggedin' in session:
        # redirect Pharmaceutical Company to dashboard
        return render_template('pharma_dashboard.html', name=session['name'])
    # if not redirect to the login page
    return redirect(url_for('pharma_login'))

@app.route('/pharma_profile', methods=['GET', 'POST'])
def pharma_profile():
    # verify if the Pharmaceutical Company is logged in
    if 'loggedin' in session:
        # redirect Pharmaceutical Company to dashboard
        return render_template('pharma_profile.html', name=session['name'])
    # if not redirect to the login page
    return redirect(url_for('pharma_login'))

@app.route('/add_drug', methods=['GET', 'POST'])
def add_drug():
    # verify if the Pharmaceutical Company is logged in
    if 'loggedin' in session:

        output = ' '
        if request.method == 'POST':
            drug_name = request.form['drug_name']
            uses = request.form['uses']
            side_effect = request.form['side_effect']

            #mysql query
            mycursor = link.cursor()
            mycursor.execute('SELECT Name FROM Drugs WHERE Name = %s', (drug_name,))
            drug_nameCheck = mycursor.fetchone()

            if drug_nameCheck:
                output = 'Drug already exists!'
            else:
                mycursor.execute('INSERT INTO Drugs (Name, Uses, SideEffect, P_Id) VALUES (%s, %s, %s, (SELECT P_Id FROM Pharmaceuticals WHERE Name= %s))', (drug_name, uses, side_effect, session["name"]) )
                link.commit()
                output = 'Drug added successfully!!!'



        # redirect Pharmaceutical Company to dashboard
        return render_template('add_drug.html', name=session['name'], output = output)
    # if not redirect to the login page
    return redirect(url_for('pharma_login'))

@app.route('/pharma_view_drug', methods=['GET', 'POST'])
def pharma_view_drug():
    # verify if the Pharmaceutical Company is logged in
    if 'loggedin' in session:
        # redirect Pharmaceutical Company to dashboard
        return render_template('pharma_view_drug.html', name=session['name'])
    # if not redirect to the login page
    return redirect(url_for('pharma_login'))

@app.route('/pharma_logout')
def pharma_logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('name', None)
   # Redirect to login page
   return redirect(url_for('pharma_login'))

if __name__ == '__main__':
    app.run()
