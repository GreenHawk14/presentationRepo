from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_stylists import Stylist
from flask_app.models.models_customers import Customer
from flask_app.models.models_appointments import Appointment
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/stylist-login')
def loginStyle():
    return render_template('stylist_login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register-stylist', methods=["POST"])
def register_stylist():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'username' : request.form['username'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'pw_config' : request.form['pw_config']
    }
    valid = Stylist.stylist_validator(data)
    if valid:
        stylist = Stylist.stylist_create(data)
        session['stylist_id'] = stylist
        print(f"Confirmation - Stylist: {stylist}, has been added.")
        return redirect('/stylistDash')

    return redirect('/stylist-login')

@app.route('/login_stylist', methods=['POST'])
def stylist_login():
    data = {
        'username' : request.form['username']
    }

    stylist = Stylist.locateStylist_viaUsername(data)

    if not stylist:
        flash("Invalid username", 'loginST')
        return redirect('/stylist-login')
    if not bcrypt.check_password_hash(stylist.password, request.form['password']):
        flash("Invalid password", 'loginST')
        return redirect('/stylist-login')

    session['stylist_id'] = stylist.id

    print('<<<<<<<<<<<<<<<<<<< processing >>>>>>>>>>>>>>>>>>')
    print('<<<<<<<<<.......Login Successful.......>>>>>>>>>>')

    return redirect('/stylistDash')

@app.route('/stylistDash')
def stylist_Dash():
    if 'stylist_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['stylist_id']
    }
    barber = Stylist.findStylist(data)
    return render_template('stylist_dashboard.html', barber = barber)

@app.route('/edit/Stylist/<int:stylist_id>')
def editStylist(stylist_id):
    data = {
        'id': stylist_id
    }
    lookup = Stylist.findStylist(data)
    return render_template('stylist_edit.html', lookup = lookup)

@app.route('/update_Stylist/<int:Stylist_id>', methods=['POST'])
def stylistUpdated(Stylist_id):
    data = {
        'id' : Stylist_id,
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'username' : request.form['username'],
        'email' : request.form['email'],
        'contact' : request.form['contact'],
        'img' : request.form['img'],
        'category' : request.form['category']
    }
    Stylist.update_stylist(data)
    print('Details have been updated...')
    return redirect('/stylistDash')