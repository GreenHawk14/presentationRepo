from flask_app import app
from flask_app.controllers import controllers_stylists, controllers_appointments, controllers_customers

if __name__ == '__main__':
    app.run(debug=True)