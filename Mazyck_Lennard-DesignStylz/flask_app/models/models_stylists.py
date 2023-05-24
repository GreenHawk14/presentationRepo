from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt

db = 'salon_db'
bcrypt = Bcrypt(app)

class Stylist:

        def __init__(self, data):
                self.id = data['id']
                self.first_name = data['first_name']
                self.last_name = data['last_name']
                self.username = data['username']
                self.password = bcrypt.generate_password_hash(data['password'])
                self.email = data['email']
                self.contact = data['contact']
                self.img = data['img']
                self.created_at = data['created_at']
                self.updated_at = data['updated_at']

        @classmethod
        def stylist_create(cls, data):
                query = """
                        INSERT INTO stylist (first_name, last_name, username, email, password)
                        VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s);
                        """
                print("query", query)
                return connectToMySQL(db).query_db(query, data)

        @classmethod
        def update_stylist(cls, data):
                query = """
                        UPDATE stylist
                        SET first_name = %(first_name)s, last_name = %(last_name)s,  username = %(username)s, password = %(password)s,
                        email = %(email)s, contact = %(contact)s, image = %(image)s
                        WHERE id = %(id)s;
                        """
                print("query", query)
                return connectToMySQL(db).query_db(query, data)

        @classmethod
        def locateStylist_viaUsername(cls,data):
                query = """
                        SELECT * FROM stylist
                        WHERE username = %(username)s
                        """
                result = connectToMySQL(db).query_db(query, data)
                print('query', query)
                if len(result) < 1:
                        return False
                return Stylist(result[0])

        @classmethod
        def findStylist (cls, data):
                query = """
                        SELECT * FROM stylist
                        WHERE id = %(id)s
                        """
                result = connectToMySQL(db).query_db(query, data)
                print('query', query)
                return cls(result[0])

        @classmethod
        def allStylist(cls):
                query = "SELECT * FROM stylist;"
                results = connectToMySQL(db).query_db(query)
                stylist_cat = []
                print("stylists", results)
                for hairdresser in results:
                        stylist_cat.append(cls(hairdresser))
                return stylist_cat

        @staticmethod
        def stylist_validator(data):
                PASSWORD_REGEX = re.compile(r'^[a-zA-Z]\w{3,14}$')
                EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
                is_valid = True

                if len(data['first_name']) < 2:
                        flash("First Name - letters only, at least 2 characters and that it was submitted.", 'registerST')
                        is_valid = False
                if len(data['last_name']) < 2:
                        flash("Last Name - letters only, at least 2 characters and that it was submitted.", 'registerST')
                        is_valid = False
                if len(data['username']) < 6:
                        flash("Username - at least 6 characters or more.", 'registerST')
                        is_valid = False
                if not EMAIL_REGEX.match(data['email']):
                        flash("Invalid email format.", 'registerST')
                        is_valid = False
                if data['password'] != data['pw_config']:
                        flash("password does not match", 'registerST')
                        is_valid = False

                return is_valid