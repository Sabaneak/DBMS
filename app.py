import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
import pymysql

from resources.user import Prisoner_Login, Official_Login, Business_Login, Relative_Login, User_Logout
from resources.reports import (
    PrisonerReport, GuardReport, WardenReport, PrisonReport, ChoreSheet, ChiefWardenReport, AdminReport,
    RelativeSheet, BusinessSheet, VisitSheet, PrisonerPrison, PrisonerBusiness,BusinessRequirement,UpdateRequirement, 
    GuardWarden, GuardChiefWarden, WardenChiefWarden, ChiefWardenAdmin, BusinessAll
)

from resources.chore import Chore, ChorePrison
from resources.shift import ShiftAssignment
from resources.facility import Facility
from resources.relative import Relative, RelativePrison
from resources.visit import Visit
from resources.business import Business
from resources.prison import Prison, Prisons_All
from resources.prisoner import Prisoner, Prisoners, AddPrisonerComponents
from resources.crime import Crime, Crime_Records
from resources.official import Official, Wardens, Guards

from resources.upload import Upload

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

api.add_resource(PrisonerReport, '/prisoner_report/<int:pid>')
api.add_resource(GuardReport, '/guard_report/<int:_id>')
api.add_resource(WardenReport, '/warden_report/<int:_id>')
api.add_resource(PrisonReport, '/prison_report/<int:pno>')
api.add_resource(ChoreSheet, '/chore_sheet/<int:pno>')
api.add_resource(ChiefWardenReport, '/chief_warden_report/<int:_id>')
api.add_resource(AdminReport, '/admin_report/<int:_id>')
api.add_resource(RelativeSheet, '/relative_sheet/<int:rid>')
api.add_resource(BusinessSheet, '/business_sheet/<int:bid>')
api.add_resource(BusinessAll, '/business_registered')
api.add_resource(VisitSheet, '/visit_sheet/<int:prison_no>')
api.add_resource(PrisonerPrison, '/prisoner_prison/<int:prison_no>')
api.add_resource(PrisonerBusiness,'/prisoner_business/<int:bid>')
api.add_resource(GuardWarden, '/guard_warden/<int:empid>')
api.add_resource(GuardChiefWarden, '/guard_chief_warden/<int:pno>')
api.add_resource(WardenChiefWarden, '/warden_chief_warden/<int:empid>')
api.add_resource(ChiefWardenAdmin, '/chief_warden_admin/<int:empid>')
api.add_resource(BusinessRequirement,'/business_requirement/<int:bid>')
api.add_resource(UpdateRequirement, '/update_business_requirement/<int:bid>')

api.add_resource(Chore, '/chore')
api.add_resource(ChorePrison, '/chore_prison/<int:pno>')
api.add_resource(ShiftAssignment, '/shift/<int:_id>')
api.add_resource(Facility, '/facility/<int:pno>')
api.add_resource(Relative, '/relative/<int:pid>')
api.add_resource(RelativePrison, '/relative_prison/<int:pno>')
api.add_resource(Visit, '/visit')

api.add_resource(Prison, '/prison/<int:pno>')
api.add_resource(Prisons_All, '/prison/all')
api.add_resource(Business, '/business/<int:bus_id>')

api.add_resource(Prisoner, '/prisoner/<int:pid>')
api.add_resource(Prisoners, '/prisoners/all/<int:_id>')
api.add_resource(AddPrisonerComponents, '/prisoner_form_details/<int:pno>')

api.add_resource(Crime, '/crime/<int:cid>')
api.add_resource(Crime_Records, '/crime_records/<int:pid>')

api.add_resource(Official, '/official/<int:empid>')
api.add_resource(Wardens, '/official/wardens/<int:_id>')
api.add_resource(Guards, '/official/guards/<int:_id>')

# api.add_resource(Upload, '/upload/<int:tid>')

if __name__ == '__main__':
    app.run(debug=True)