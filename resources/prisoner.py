from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple


class Prisoner(Resource):
    @jwt_required()
    def post(self, pid):
        body = request.get_json()
        sql = "INSERT INTO prisoner (pid, password, first_name, last_name, age, ht_in_m, wt_in_kg, eye_colour, " \
              "hair_colour, fingerprint, visits_made, prison_no, employed_by, entry_date) VALUES (%s %s %s %s %s %s %s %s %s %s %s %s %s %s)"
        tuple = (
        pid, body['password'], body['first_name'], body['last_name'], body['age'], body['ht_in_m'], body['wt_in_kg'],
        body['eye_colour'],
        body['hair_colour'], body['fingerprint'], body['visits_made'], body['prison_no'], body['employed_by'],
        body['entry_date'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Prisoner added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self, pid):
        sql = "DELETE FROM prisoner WHERE pid = %s"
        tuple = (pid)

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Prisoner deleted'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def put(self, pid):
        body = request.get_json()
        sql = "UPDATE prisoner SET prison_no = %s WHERE pid = %s"
        tuple = (body['pno'], pid)

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Prisoner {} shifted to prison {}'.format(pid, body['pno'])}, 200
        except Exception as e:
            return {'msg': str(e)}, 400


class Prisoners(Resource):
    @jwt_required()
    def get(self):
        sql = "SELECT p.pid, p.first_name, p.last_name, c.c_name FROM prisoner p, crime c, crime_records cr WHERE p.pid = cr.pid AND cr.cid = c.cid"
        res = execute_sql(sql=sql)

        if res == "[]":
            return {'msg': 'No prisoners'}, 400
        else:
            return {'Prisoners': res}, 200


class Prisoner_ID(Resource):
    @jwt_required()
    def post(self, pid):
        body = request.get_json()
        sql = "INSERT INTO prisoner_id_marks (pid, identifying_mark) VALUES (%s, %s)"
        tuple = (pid, [body['identifying_mark'][i] for i in range(len(body['identifying_mark']))])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Prisoner {}'.format(pid)}, 200
        except Exception as e:
            return {'msg': str(e)}, 400


class Prisoner_Affiliations(Resource):
    @jwt_required()
    def post(self, pid):
        body = request.get_json()
        sql = "INSERT INTO prisoner_affiliations (p_1, p_2) VALUES (%s, %s)"
        tuple = (pid, body['p_2'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Prisoner {}'.format(pid)}, 200
        except Exception as e:
            return {'msg': str(e)}, 400
