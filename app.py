from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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
@app.route('/admin_register')
def admin_register():
    return render_template('admin_register.html')

if __name__ == '__main__':
    app.run()
