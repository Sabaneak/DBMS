from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple

class Chore(Resource):
    @jwt_required()
    def post(self):
        body = request.get_json()
        sql = "INSERT INTO prisoner_chores (pid, prison_no, chore_name) VALUES (%s, %s, %s)"
        tuple = (body['pid'], body['prison_no'], body['chore_name'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Chore added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self):
        body = request.get_json()
        sql = "DELETE FROM prisoner_chores WHERE pid = %s AND prison_no = %s AND chore_name = %s"
        tuple = (body['pid'], body['prison_no'], body['chore_name'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Chore deleted'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

class ShiftAssignment(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT * FROM guard_shifts s, official o WHERE s.empid = o.empid AND o.prison_no = %s"
        tuple = (_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prison does not exist'}, 400
        else:
            return {'Prison {}'.format(_id): res}, 200

    @jwt_required()
    def post(self, _id):
        body = request.get_json()
        sql = "INSERT INTO guard_shifts(empid, shift_number) VALUES (% s, % s)"
        tuple = (_id, body['shift_number'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Chore added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self, _id):
        sql = "DELETE FROM guard_shifts WHERE empid = % s"
        tuple = (_id)

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Chore deleted'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

class Facility(Resource):
    @jwt_required()
    def get(self, pno):
        sql = "SELECT * FROM prison_facilities WHERE prison_no = %s"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prison does not exist'}, 400
        else:
            return {'Prison {}'.format(_id): res}, 200

    @jwt_required()
    def post(self, pno):
        body = request.get_json()
        sql = "INSERT INTO prison_facilities (prison_no, facility_name, cost_per_unit_monthly, count) VALUES (%s, %s, %s, %s)"
        tuple = (pno, body['facility_name'], body['cost_per_unit_monthly'], body['count'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Facility added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self, pno):
        body = request.get_json()
        sql = "DELETE FROM prison_facilities WHERE prison_no = %s AND facility_name = %s"
        tuple = (_id, body['facility_name'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Facility deleted'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def put(self, pno):
        body = request.get_json()
        sql = "UPDATE prison_facilities SET count = %s WHERE prison_no = %s AND facility_name = %s"
        tuple = (body['count'], pno, body['facility_name'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Facility updated'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

class Relative(Resource):
    @jwt_required()
    def get(self, pid):
        sql = "SELECT rid, relation, r.first_name, r.last_name, p.pid AS prisoner FROM prisoner p, relative r WHERE r.pid = p.pid AND r.pid = %s"
        tuple = (pid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Relative does not exist'}, 400
        else:
            return {'Relative of prisoner {}'.format(pid): res}, 200

    @jwt_required()
    def post(self, pid):
        body = request.get_json()
        sql = "INSERT INTO relative (rid, password, pid, relation, first_name, last_name) VALUES (%s, %s, %s, %s, %s, %s)"
        tuple = (body['rid'], body['password'], pid, body['relation'], body['first_name'], body['last_name'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Relative added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self, pid):
        body = request.get_json()
        sql = "DELETE FROM relative WHERE rid = %s and pid = %s"
        tuple = (body['rid'], pid)

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Relative deleted'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

class Visit(Resource):
    @jwt_required()
    def post(self):
        body = request.get_json()
        sql = "INSERT INTO visit (vid, rid, date) VALUES (%s %s %s)"
        tuple = (body['vid'], body['rid'], body['date'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Visit added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400



