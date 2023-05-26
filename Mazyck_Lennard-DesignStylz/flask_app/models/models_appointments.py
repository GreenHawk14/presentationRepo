from flask_app.config.mysqlconnection import connectToMySQL
from flask import session
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app.models import models_customers
from flask_app.models import models_stylists
import pprint

db = 'salon_db'
bcrypt = Bcrypt(app)

class Appointment:

        def __init__(self, data):
                self.id = data['id']
                self.date = data['date']
                self.time = data['time']
                self.description = data['description']
                self.service = data['service'].split(";")
                self.created_at = data['created_at']
                self.updated_at = data['updated_at']
                self.customer = None
                self.stylist = None

        @classmethod
        def appointment_create(cls, data):
                query  = """
                        INSERT INTO appointment (date, time, description, service, customer_id, stylist_id)
                        VALUES (%(date)s, %(time)s, %(description)s, %(service)s, %(customer_id)s, %(stylist_id)s);
                        """
                print("query", query)
                return connectToMySQL(db).query_db(query, data)

        @classmethod
        def lookup_Appt(cls, data):
                query = """
                        SELECT * from appointment
                        WHERE id = %(id)s;
                        """
                result = connectToMySQL(db).query_db(query,data)
                return cls(result[0])

        @classmethod
        def locateAppointment_viaLastName(cls,data):
                query = """
                        SELECT * FROM appointment
                        WHERE Last_name = %(Last_name)s;
                        """
                result = connectToMySQL(db).query_db(query, data)
                print('query', query)
                if len(result) < 1:
                        return False
                return cls(result[0])

        @classmethod
        def update_appt(cls, data):
                query = """
                        UPDATE appointment
                        SET date = %(date)s, time = %(time)s, description = %(description)s, service = %(service)s,
                        WHERE id = %(id)s;
                        """
                print("query", query)
                return connectToMySQL(db).query_db(query, data)

        @classmethod
        def destroy_appt(cls, data):
                query = """
                        DELETE FROM appointment
                        WHERE id = %(id)s;
                        """
                return connectToMySQL(db).query_db(query, data)

        @classmethod
        def getStylistWithAppts(cls, data):
                query = """
                        SELECT * from stylist
                        LEFT JOIN appointment
                        ON stylist.id = appointment.stylist_id
                        WHERE stylist.id = %(id)s;
                        """
                results = connectToMySQL(db).query_db(query, data)
                stylist = models_stylists.Stylist(results[0])
                print(len(results))
                if results[0]['appointment.id'] == None:
                        print('APPT')
                        return stylist
                for detail in results:
                        appointment_data = {
                                'id' : detail['appointment.id'],
                                'date' : detail['date'],
                                'time': detail['time'],
                                'description': detail['description'],
                                'service': detail['service'],
                                'created_at': detail['appointment.created_at'],
                                'updated_at': detail['appointment.updated_at']
                        }
                        stylist.appointment.append(cls(appointment_data))

                return stylist

        @classmethod
        def getApptsbyID(cls, data):
                query = """
                        SELECT * from appointment
                        LEFT JOIN customer
                        ON customer.id = appointment.customer_id
                        WHERE appointment.id = %(id)s;
                        """
                results = connectToMySQL(db).query_db(query, data)
                print("RESULTS ------>", results)
                appointment = cls(results[0])
                customer_data = {
                        'id' : results[0]['customer_id'],
                        'first_name' : results[0]['first_name'],
                        'last_name' : results[0]['last_name'],
                        'email' : results[0]['email'],
                        'username' : results[0]['username'],
                        'password' : results[0]['password'],
                        'contact' : results[0]['contact'],
                        'address' : results[0]['address'],
                        'created_at': results[0]['customer.created_at'],
                        'updated_at': results[0]['customer.updated_at']
                }
                appointment.customer = models_customers.Customer(customer_data)
                return appointment

        @classmethod
        def getCustomersWithAppts(cls, data):
                query = """
                        SELECT * from customer
                        LEFT JOIN appointment
                        ON customer.id = appointment.customer_id
                        WHERE customer.id = %(id)s;
                        """
                results = connectToMySQL(db).query_db(query, data)
                print("RESULTS** ------>", results)
                customer = models_customers.Customer(results[0])
                print(len(results))
                if results[0]['appointment.id'] == None:
                        print('APPT')
                        return customer
                for page in results:
                        appointment_data = {
                                'id' : page['appointment.id'],
                                'date' : page['date'],
                                'time': page['time'],
                                'description': page['description'],
                                'service': page['service'],
                                'created_at': page['appointment.created_at'],
                                'updated_at': page['appointment.updated_at']
                        }
                        customer.appointment.append(cls(appointment_data))
                return customer

        @staticmethod
        def appointment_validator(data):
                is_valid = True

                if data['date'] == '':
                        flash("Scheduling an appointment requires a DATE to be posted.", 'appointment')
                        is_valid = False
                if data['time'] == '':
                        flash("Scheduling an appointment requires a TIME to be posted.", 'appointment')
                        is_valid = False
                if data['service'] == '':
                        flash("What SERVICE are we providing?", 'appointment')
                        is_valid = False

                return is_valid