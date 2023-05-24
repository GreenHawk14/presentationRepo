from flask_app.config.mysqlconnection import connectToMySQL
from flask import session
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt

db = 'salon_db'
bcrypt = Bcrypt(app)

class Appointment:

        def __init__(self, data):
                self.id = data['id']
                self.date = data['date']
                self.time = data['time']
                self.description = data['description']
                self.service = data['service']
                self.image = data['image']
                self.created_at = data['created_at']
                self.updated_at = data['updated_at']
                self.bulletin = []

        @classmethod
        def appointment_create(cls, data):
                query  = """
                        INSERT INTO appointment (date, time, description, service, image, customer_id, stylist_id)
                        VALUES (%(date)s, %(time)s, %(description)s, %(service)s, %(image)s, %(customer_id)s, %(stylist_id)s);
                        """
                print("query", query)
                return connectToMySQL(db).query_db(query, data)

        @classmethod
        def lookup_Appt(cls, data):
                query = """
                        SELECT * from appointment
                        WHERE id = %(id)s
                        """
                result = connectToMySQL(db).query_db(query,data)

        @classmethod
        def locateAppointment_viaLastName(cls,data):
                query = """
                        SELECT * FROM appointment
                        WHERE Last_name = %(Last_name)s
                        """
                result = connectToMySQL(db).query_db(query, data)
                print('query', query)
                if len(result) < 1:
                        return False
                return Appointment(result[0])

        @classmethod
        def update_appt(cls, data):
                query = """
                        UPDATE appointment
                        SET date = %(date)s, time = %(time)s, description = %(description)s, service = %(service)s, image = %(image)s
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
        def apptDataOFcustomers(cls, data):
                query = """
                        SELECT * from appointment
                        LEFT JOIN customer
                        ON customer.id = appointment.customer_id;
                        WHERE appointment.id = %(id)s
                        """
                results = connectToMySQL(db).query_db(query,data)
                catalog = []
                for detail in results:
                        page = cls(detail)
                        customer_data = {
                                'id' : session['customer_id'],
                                'first_name' : detail['first_name'],
                                'last_name' : detail['last_name'],
                                'email' : detail['email'],
                                'username' : detail['username'],
                                'password' : detail['password'],
                                'contact' : detail['contact'],
                                'address' : detail['address'],
                                'created_at' : detail['created_at'],
                                'updated_at' : detail['updated_at']
                        }
                        page.bulletin = Appointment(customer_data)
                        catalog.append(page)
                return catalog

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