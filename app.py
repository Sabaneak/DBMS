import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
import pymysql
from resources.resources import Prisoner
from resources.user import Prisoner_Login, Official_Login, Business_Login, Relative_Login, User_Logout

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.urandom(24)
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Prisoner_Login, '/prisoner_login')
api.add_resource(Official_Login, '/official_login')
api.add_resource(Business_Login, '/business_login')
api.add_resource(Relative_Login, '/relative_login')
api.add_resource(User_Logout, '/logout')


if __name__ == '__main__':
    app.run(debug=True)