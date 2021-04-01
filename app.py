import os
from flask import Flask
from flask_restful import Api
from db import db
import pymysql
from resources.resources import Prisoner

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
api = Api(app)
api.add_resource(Prisoner, '/Prisoner')


if __name__ == '__main__':
    app.run(debug=True)