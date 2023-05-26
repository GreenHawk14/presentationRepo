from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt

db = 'salon_db'
bcrypt = Bcrypt(app)

class Customer:

        def __init__(self, data):
                self.id = data['id']
                self.first_name = data['first_name']
                self.last_name = data['last_name']
                self.email = data['email']
                self.username = data['username']
                self.password = bcrypt.generate_password_hash(data['password'])
                self.contact = data['contact']
                self.address = data['address']
                self.created_at = data['created_at']
                self.updated_at = data['updated_at']
                self.appointments = []

        @classmethod
        def create_customer(cls, data):
                query = """
                        INSERT INTO customer (first_name, last_name, email, username, password)
                        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(username)s, %(password)s);
                        """
                print("query", query)
                return connectToMySQL(db).query_db(query, data)

        @classmethod
        def update_customer(cls, data):
                query = """
                        UPDATE customer
                        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, username = %(username)s,
                        contact = %(contact)s, address = %(address)s
                        WHERE id = %(id)s;
                        """
                print("query", query)
                return connectToMySQL(db).query_db(query, data)

        @classmethod
        def locateCustomer_viaUsername(cls,data):
                query = """
                        SELECT * FROM customer
                        WHERE username = %(username)s
                        """
                result = connectToMySQL(db).query_db(query, data)
                print('query', query)
                if len(result) < 1:
                        return False
                return Customer(result[0])

        @classmethod
        def findCustomer (cls, data):
                query = """
                        SELECT * FROM customer
                        WHERE id = %(id)s
                        """
                result = connectToMySQL(db).query_db(query, data)
                print('query', query)
                return cls(result[0])

        @staticmethod
        def customer_validator(data):
                PASSWORD_REGEX = re.compile(r'^[a-zA-Z]\w{3,14}$')
                EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
                is_valid = True

                if len(data['first_name']) < 3:
                        flash("First Name - letters only, at least 3 characters or more.", 'registerCU')
                        is_valid = False
                if len(data['last_name']) < 2:
                        flash("Last Name - letters only, at least 2 characters or more.", 'registerCU')
                        is_valid = False
                if len(data['username']) < 6:
                        flash("Username - at least 6 characters or more.", 'registerCU')
                        is_valid = False
                if not EMAIL_REGEX.match(data['email']):
                        flash("Invalid email format.", 'registerCU')
                        is_valid = False
                if data['password'] != data['pw_config']:
                        flash("password does not match", 'registerCU')
                        is_valid = False

                return is_valid