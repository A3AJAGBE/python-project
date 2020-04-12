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

#This is to display the users about page of the website.
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


#This will allow users search for drugs using name, uses, side effect, and Pharmaceutical name
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']

        #mysql query to retrieve data from the database for search functionality
        mycursor = link.cursor()
        mycursor.execute('SELECT D.Name, D.Uses, D.SideEffect, P.Name FROM Pharmaceuticals P INNER JOIN Drugs D ON P.P_Id = D.P_Id WHERE D.Name LIKE %s OR D.Uses Like %s OR D.SideEffect LIKE %s OR P.Name LIKE %s', ('%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%'))
        result = mycursor.fetchall()

        # redirect user to the result page
        return render_template('search.html', result = result)

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

#This will allow Administrator see their profile
@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    # verify if the Administratoris logged in
    if 'loggedin' in session:

        #mysql query to retrieve Administrator data
        mycursor = link.cursor()
        mycursor.execute('SELECT Name, Username FROM Administrators WHERE Username = %s', (session['username'],))
        profile = mycursor.fetchone()

        # redirect Administrator to their profile page
        return render_template('admin_profile.html', profile = profile)

    # if not redirect to the login page
    return redirect(url_for('admin_main'))

#This will allow Administrator to view new Administrator requesting access
@app.route('/access_notice', methods=['GET', 'POST'])
def access_notice():
    # verify if the Administrator is logged in
    if 'loggedin' in session:

        #mysql query to retrieve data from the database
        mycursor = link.cursor()
        mycursor.execute('SELECT LoginAccess_Id, Name, Username, Email FROM LoginAccess')
        adminReq = mycursor.fetchall()

        # redirect Administrator to page where they can view all output
        return render_template('access_notice.html', username=session['username'], adminReq = adminReq)

    # if not redirect to the login page
    return redirect(url_for('admin_main'))

#This will allow Administrator to view all Pharmaceuticals information
@app.route('/view_pharma', methods=['GET', 'POST'])
def view_pharma():
    # verify if the Administrator is logged in
    if 'loggedin' in session:

        #mysql query to retrieve data from the database
        mycursor = link.cursor()
        mycursor.execute('SELECT P_Id, Name, Location FROM Pharmaceuticals')
        viewAdmin = mycursor.fetchall()

        # redirect Administrator to page where they can view all output
        return render_template('view_pharma.html', username=session['username'], viewAdmin = viewAdmin)

    # if not redirect to the login page
    return redirect(url_for('admin_main'))

#This will allow Administrator to view all the drugs in the database
@app.route('/view_drugs', methods=['GET', 'POST'])
def view_drugs():
    # verify if the Administrator is logged in
    if 'loggedin' in session:

            #mysql query to retrieve data from the database for search functionality
            mycursor = link.cursor()
            mycursor.execute('SELECT D.DrugId, D.Name, D.Uses, D.SideEffect, P.Name FROM Pharmaceuticals P INNER JOIN Drugs D ON  P.P_Id = D.P_Id')
            adminDrug = mycursor.fetchall()

            # redirect Administrator to the result page
            return render_template('view_drugs.html', username=session['username'], adminDrug = adminDrug)

    # if not redirect to the login page
    return redirect(url_for('admin_main'))

#This will allow Administrator to search for drugs using name and uses
@app.route('/admin_search', methods=['GET', 'POST'])
def admin_search():
    # verify if the Administrator is logged in
    if 'loggedin' in session:
        if request.method == 'POST':
            search = request.form['search']

            #mysql query to retrieve data from the database for search functionality
            mycursor = link.cursor()
            mycursor.execute('SELECT D.DrugId, D.Name, D.Uses, D.SideEffect, P.Name FROM Pharmaceuticals P INNER JOIN Drugs D ON  P.P_Id = D.P_Id WHERE D.Name LIKE %s OR D.Uses Like %s', ('%' + search + '%', '%' + search + '%'))
            adminDrug = mycursor.fetchall()

            # redirect Administrator to the result page
            return render_template('admin_search.html', username=session['username'], adminDrug = adminDrug)

    # if not redirect to the login page
    return redirect(url_for('admin_main'))

#This will allow Administrator to logout of the access page
@app.route('/logout')
def logout():
    # Remove session data, this will logout the Administrator
   session.pop('loggedin', None)
   session.pop('username', None)

   # Redirect to login page
   return redirect(url_for('admin_main'))


""" This is the start of Pharma route  """
#This will allow Pharmaceutical login
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

        if nameCheck:
            # Create session data
            session['loggedin'] = True
            session['name'] = name

            # Redirect to dashboard page
            return redirect(url_for('pharma_dashboard'))
        else:
            # Pharmaceutical doesn't exist or username/password is incorrect
            output = 'Incorrect login information, Try again'
    return render_template('pharma_login.html', output = output)

#This will allow Pharmaceutical register to have access
@app.route('/pharma_reg', methods=['GET', 'POST'])
def pharma_reg():

    output = ' '
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        password = hashlib.sha256(str(request.form['password']).encode('utf-8')).hexdigest()
        con_password = hashlib.sha256(str(request.form['con_password']).encode('utf-8')).hexdigest()

        #mysql query to verify that the account doesn't exists
        mycursor = link.cursor()
        mycursor.execute('SELECT name FROM Pharmaceuticals WHERE name = %s', (name,))
        nameCheck = mycursor.fetchone()

        if nameCheck:
            output = 'Account already exists!'
        else:
            mycursor.execute('INSERT INTO Pharmaceuticals (Name, Location, Password, confirmPassword) VALUES (%s, %s, %s, %s)', (name, location, password, con_password) )
            link.commit()
            output = 'Account successfully created, Go back to login page'

    # Return status of registration
    return render_template('pharma_reg.html', output = output)

#This will allow Pharmaceutical read a summary of the access page
@app.route('/pharma_dashboard', methods=['GET', 'POST'])
def pharma_dashboard():
    # verify if the Pharmaceutical Company is logged in
    if 'loggedin' in session:

        # redirect Pharmaceutical Company to dashboard
        return render_template('pharma_dashboard.html', name=session['name'])

    # if not redirect to the login page
    return redirect(url_for('pharma_login'))

#This will allow Pharmaceutical see their profile
@app.route('/pharma_profile', methods=['GET', 'POST'])
def pharma_profile():
    # verify if the Pharmaceutical Company is logged in
    if 'loggedin' in session:

        #mysql query to retrieve Pharmaceutical data
        mycursor = link.cursor()
        mycursor.execute('SELECT Name, Location FROM Pharmaceuticals WHERE Name = %s', (session['name'],))
        profile = mycursor.fetchone()

        # redirect Pharmaceutical Company to their profile page
        return render_template('pharma_profile.html', profile = profile)

    # if not redirect to the login page
    return redirect(url_for('pharma_login'))

#This will allow Pharmaceutical to add drugs in the database
@app.route('/add_drug', methods=['GET', 'POST'])
def add_drug():
    # verify if the Pharmaceutical Company is logged in
    if 'loggedin' in session:

        output = ' '
        if request.method == 'POST':
            drug_name = request.form['drug_name']
            uses = request.form['uses']
            side_effect = request.form['side_effect']

            #mysql query to very that the drug is not in the database
            mycursor = link.cursor()
            mycursor.execute('SELECT Name FROM Drugs WHERE Name = %s', (drug_name,))
            drug_nameCheck = mycursor.fetchone()

            if drug_nameCheck:
                output = 'Drug already exists!'
            else:
                mycursor.execute('INSERT INTO Drugs (Name, Uses, SideEffect, P_Id) VALUES (%s, %s, %s, (SELECT P_Id FROM Pharmaceuticals WHERE Name= %s))', (drug_name, uses, side_effect, session["name"]) )
                link.commit()
                output = 'Drug added successfully!!!'

        # redirect Pharmaceutical to the page where they can add drugs
        return render_template('add_drug.html', name=session['name'], output = output)

    # if not redirect to the login page
    return redirect(url_for('pharma_login'))

#This will allow Pharmaceutical to view all drugs in the database made by the company
@app.route('/pharma_view_drug', methods=['GET', 'POST'])
def pharma_view_drug():
    # verify if the Pharmaceutical Company is logged in
    if 'loggedin' in session:

        #mysql query to retrieve data from the database to display drugs made by the Pharmaceutical
        mycursor = link.cursor()
        mycursor.execute('SELECT DrugId, Name, Uses, SideEffect FROM Drugs WHERE P_Id IN (SELECT P_Id FROM Pharmaceuticals WHERE Name= %s)', (session['name'],))
        pharmaDrug = mycursor.fetchall()

        # redirect Pharmaceutical to page where they can view all their drugs in the database
        return render_template('pharma_view_drug.html', name=session['name'], pharmaDrug = pharmaDrug)

    # if not redirect to the login page
    return redirect(url_for('pharma_login'))

#This will allow Pharmaceutical to search for drugs using name only they will get result if the drug is made by them
@app.route('/pharma_search', methods=['GET', 'POST'])
def pharma_search():
    # verify if the Pharmaceutical is logged in
    if 'loggedin' in session:
        if request.method == 'POST':
            search = request.form['search']

            #mysql query to retrieve data from the database for search functionality
            mycursor = link.cursor()
            mycursor.execute('SELECT DrugId, Name, Uses, SideEffect FROM Drugs WHERE Name LIKE %s AND P_Id IN (SELECT P_Id FROM Pharmaceuticals WHERE Name= %s)', ('%' + search + '%', session['name']))
            pharmaDrug = mycursor.fetchall()

            # redirect Pharmaceutical to the result page
            return render_template('pharma_search.html', name=session['name'], pharmaDrug = pharmaDrug)

    # if not redirect to the login page
    return redirect(url_for('pharma_login'))

#This will allow Pharmaceutical to logout of the access page
@app.route('/pharma_logout')
def pharma_logout():
    # Remove session data, this will logout the Pharmaceutical
   session.pop('loggedin', None)
   session.pop('name', None)

   # Redirect to Pharmaceutical login page
   return redirect(url_for('pharma_login'))


if __name__ == '__main__':
    app.run()
