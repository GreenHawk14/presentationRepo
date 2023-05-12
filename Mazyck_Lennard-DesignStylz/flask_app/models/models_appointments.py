from flask_app.config.mysqlconnection import connectToMySQL
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

        @classmethod
        def appointment_create(cls, data):
                query  = """
                        INSERT INTO appointment (date, time, description, service, image, stylist_id, customer_id)
                        VALUES (%(date)s, %(time)s, %(description)s, %(service)s, %(image)s, %(stylist_id)s, %(customer_id)s);
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
        def update_appt(cls, data):
                query = """
                        UPDATE appointment
                        SET date = %(date)s, time = %(time)s, description = %(description)s, service = %(service)s, image = %(image)s
                        WHERE id = %(id)s;
                        """
                print("query", query)
                return connectToMySQL(db).query_db(query, data)

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

        @staticmethod
        def appointment_validator(data):
                is_valid = True

                if data['date'] == '':
                        flash("Scheduling an appointment requires a DATE to be posted.", 'register')
                        is_valid = False
                if data['time'] == '':
                        flash("Scheduling an appointment requires a TIME to be posted.", 'appointment')
                        is_valid = False
                if data['service'] == '':
                        flash("What SERVICE are we providing?", 'register')
                        is_valid = False

                return is_valid