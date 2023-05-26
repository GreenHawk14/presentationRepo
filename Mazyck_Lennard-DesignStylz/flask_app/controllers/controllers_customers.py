from flask_app import app
from flask import render_template, redirect, request, session, flash, Flask
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_stylists import Stylist
from flask_app.models.models_customers import Customer
from flask_app.models.models_appointments import Appointment
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/customer-login')
def loginCustomer():
    return render_template('customer_login.html')

@app.route('/Team')
def teamLog():
    employee = Stylist.allStylist()
    return render_template('stylist_list.html', employee = employee)

@app.route('/register_customer', methods=["POST"])
def register_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'username' : request.form['username'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'pw_config' : request.form['pw_config']
    }
    valid = Customer.customer_validator(data)
    if valid:
        customer = Customer.create_customer(data)
        session['customer_id'] = customer
        print(f"Confirmation - Customer: {customer}, has been added.")
        return redirect('/customerDash')

    return redirect('/customer-login')

@app.route('/login_customer', methods=['POST'])
def customer_login():
    data = {
        'username' : request.form['username']
    }

    customer = Customer.locateCustomer_viaUsername(data)

    if not customer:
        flash("Invalid username", 'loginCU')
        return redirect('/customer-login')
    if not bcrypt.check_password_hash(customer.password, request.form['password']):
        flash("Invalid password", 'loginCU')
        return redirect('/customer-login')

    session['customer_id'] = customer.id

    print('<<<<<<<<<<<<<<<<<<< processing >>>>>>>>>>>>>>>>>>')
    print('<<<<<<<<<.......Login Successful.......>>>>>>>>>>')

    return redirect('/customerDash')

@app.route('/customerDash')
def customer_Dash():
    if 'customer_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['customer_id']
    }
    print(session['customer_id'], "--------------------------")
    print("data ########", data)
    #client = Customer.findCustomer(data)
    customer = Appointment.getCustomersWithAppts(data)
    return render_template('customer_dashboard.html', customer = customer)

@app.route('/edit/Customer/<int:customer_id>')
def editCustomer(customer_id):
    data = {
        'id': customer_id
    }
    clientSearch = Customer.findCustomer(data)
    return render_template('customer_edit.html', clientSearch = clientSearch)

@app.route('/customerUpdate/<int:Customer_id>', methods=['POST'])
def customerUpdated(Customer_id):
    print(request.form)
    data = {
        'id' : Customer_id,
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'username' : request.form['username'],
        'email' : request.form['email'],
        'contact' : request.form['contact'],
        'address' : request.form['address']
    }
    Customer.update_customer(data)
    print('Details have been updated...')
    return redirect('/customerDash')