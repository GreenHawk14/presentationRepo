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

@app.route('/Appt_details')
def displayDetails():
    return render_template('appt_details.html')

@app.route('/Appt_setup')
def setupAppointment():
    return render_template('create_appointment.html')

@app.route('/createAPP', methods=["POST"])
def Appt_setup():
    data = {
        'date' : request.form['date'],
        'time' : request.form['time'],
        'description' : request.form['description'],
        'service' : request.form['service'],
        'image' : request.form['image']
    }