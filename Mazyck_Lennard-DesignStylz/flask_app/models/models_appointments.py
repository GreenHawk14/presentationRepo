from flask_app.config.mysqlconnection import connectToMySQL
from flask import session
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app.models import models_customers
from flask_app.models import models_stylists

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
                        WHERE stylist_id = %(id)s;
                        """
                results = connectToMySQL(db).query_db(query, data)
                stylist = models_stylists.Stylist(results[0])
                for detail in results:
                        appointment_data = {
                                'id' : detail['id'],
                                'date' : detail['date'],
                                'time': detail['time'],
                                'description': detail['description'],
                                'service': detail['service'],
                                'created_at': detail['created_at'],
                                'updated_at': detail['updated_at']
                        }
                        stylist.appointment.append(cls(appointment_data))

                return stylist
        @classmethod
        def getCustomersWithAppts(cls, data):
                query = """
                        SELECT * from customer
                        LEFT JOIN appointment
                        ON customer.id = appointment.customer_id
                        WHERE customer_id = %(id)s;
                        """
                results = connectToMySQL(db).query_db(query, data)
                print("RESULTS ------>", results)
                customer = models_customers.Customer(results[0])
                for page in results:
                        appointment_data = {
                                'id' : page['id'],
                                'date' : page['date'],
                                'time': page['time'],
                                'description': page['description'],
                                'service': page['service'],
                                'created_at': page['created_at'],
                                'updated_at': page['updated_at']
                        }
                        customer.appointments.append(cls(appointment_data))
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