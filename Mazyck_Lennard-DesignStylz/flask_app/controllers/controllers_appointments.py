from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_stylists import Stylist
from flask_app.models.models_customers import Customer
from flask_app.models.models_appointments import Appointment
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Stylist/<int:appointment_id>/Delete')
def destroy(appointment_id):
    data = {
        'id' : appointment_id
    }
    Appointment.destroy(data)
    return redirect('/stylistDash')

@app.route('/Appt_details')
def displayDetails():
    return render_template('appt_details.html')

@app.route('/Appt_setup')
def setupAppointment():
    styler = Stylist.allStylist()
    return render_template('appt_create.html', styler = styler)

@app.route('/appt_create', methods=["POST"])
def Appt_setup():
    data = {
        'customer_id' : session['customer_id'],
        'date' : request.form['date'],
        'time' : request.form['time'],
        'description' : request.form['description'],
        'service' : request.form['service'],
        'image' : request.form['image'],
        'stylist_id' : request.form['stylist_id'],
    }
    valid = Appointment.appointment_validator(data)
    if valid:
        Appointment.appointment_create(data)
        return redirect('/customerDash')
    return redirect('/Appt_setup')