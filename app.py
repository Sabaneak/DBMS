import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
import pymysql

from resources.user import Prisoner_Login, Official_Login, Business_Login, Relative_Login, User_Logout
from resources.reports import GuardReport, WardenReport, ChoreSheet, ChiefWardenReport
from resources.miscallaneous import Chore, ShiftAssignment, Facility, Relative, Visit

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

api.add_resource(GuardReport, '/guard_report/<int:_id>')
api.add_resource(WardenReport, '/warden_report/<int:_id>')
api.add_resource(ChoreSheet, '/chore_sheet/<int:pno>')
api.add_resource(ChiefWardenReport, '/chief_warden_report/<int:_id>')

api.add_resource(Chore, '/chore')
api.add_resource(ShiftAssignment, '/shift/<int:_id>')
api.add_resource(Facility, '/facility/<int:pno>')
api.add_resource(Relative, '/relative/<int:pid>')
api.add_resource(Visit, '/visit')

if __name__ == '__main__':
    app.run(debug=True)