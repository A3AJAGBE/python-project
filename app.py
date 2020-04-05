from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

config = mysql.connector.connect(
  user = 'root',
  password ='root',
  unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock',
  raise_on_warnings = True,
  database = 'DrugSystem'
)
myCursor = config.cursor()

""" This is to display the home page of the website """
@app.route('/')
def home():
    return render_template('index.html')

""" This is to display the dashboard page of the website """
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

""" This is to display the admin home/login page of the website """
@app.route('/admin_main')
def admin_main():
    return render_template('admin_main.html')

""" This is to display the contact page of the website to user requesting for access """
@app.route('/contact')
def contact():
    return render_template('contact.html')

""" This is to display the admin register page of the website """
@app.route('/admin_register', methods=["GET","POST"])
def admin_register():
    success = ' '
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        con_password = request.form['con_password']
        myCursor.execute("INSERT INTO Administrators (Name, Username, Password, confirmPassword) VALUES (%s, %s, %s, %s)", (name, username, password, con_password) )
        config.commit()
        # myCursor.close()
        success = 'Administrator successfully in the database'
    return render_template('admin_register.html', success = success)

myCursor.close()
config.close()


if __name__ == '__main__':
    app.run()
