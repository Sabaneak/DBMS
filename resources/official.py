from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple


class Official(Resource):
    @jwt_required()
    def post(self, empid):
        body = request.get_json()
        sql = "INSERT INTO official VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        tuple = (empid, body['password'], body['first_name'], body['last_name'], body['salary'], body['years_of_experience'],
                 body['type'], body['mgr'], body['prison_no'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Official added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self, empid):
        sql = "DELETE FROM official WHERE empid = %s"
        tuple = (empid)

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Official deleted'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

class Wardens(Resource):
    @jwt_required()
    def get(self):
        sql = "SELECT empid, first_name, last_name, prison_no FROM official WHERE type = 'Warden'"
        res = execute_sql(sql=sql)

        if res == "[]":
            return {'msg': 'No wardens'}, 400
        else:
            return {'Wardens': res}, 200

class Guards(Resource):
    @jwt_required()
    def get(self):
        sql = "SELECT empid, first_name, last_name, prison_no FROM official WHERE type = 'Guard'"
        res = execute_sql(sql=sql)

        if res == "[]":
            return {'msg': 'No guards'}, 400
        else:
            return {'Guards': res}, 200
