from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple

class GuardReport(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT s.empid, prison_no, first_name, last_name, salary, years_of_experience, mgr, shift_number FROM official o, guard_shifts s WHERE o.empid = %s AND o.empid = s.empid AND type = 'Guard'"
        tuple = (_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Guard does not exist'}, 400
        else:
            return {'Guard {}'.format(_id): res}, 200

class WardenReport(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT e1.empid, e1.prison_no, e1.first_name, e1.last_name, e1.salary, e1.years_of_experience, (SELECT count(*) FROM official e2 WHERE e2.mgr = e1.empid) AS employees FROM official e1 WHERE e1.type = 'Warden' AND e1.empid = %s"
        tuple = (_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Warden does not exist'}, 400
        else:
            return {'Warden {}'.format(_id): res}, 200

class ChoreSheet(Resource):
    @jwt_required()
    def get(self, pno):
        sql = "SELECT c.pid, c.chore_name, c1.chore_time FROM prisoner_chores c, chore c1 WHERE c.prison_no = c1.prison_no AND c.chore_name = c1.chore_name AND c.prison_no = %s"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Chores do not exist'}, 400
        else:
            return {'Prison {}'.format(pno): res}, 200

class ChiefWardenReport(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT e1.empid, e1.prison_no, e1.first_name, e1.last_name, e1.salary, e1.years_of_experience, (SELECT count(*) FROM official e2 WHERE e2.mgr = e1.empid) AS employees FROM official e1 WHERE e1.type = 'Chief Warden' AND e1.empid = %s"
        tuple = (_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Chief Warden does not exist'}, 400
        else:
            return {'Chief Warden {}'.format(_id): res}, 200