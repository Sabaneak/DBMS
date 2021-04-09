from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple


class Prisoner(Resource):
    @jwt_required()
    def post(self, empid):
        body = request.get_json()
        sql = "INSERT INTO official (empid, password, first_name, last_name, salary, years_of_experience, type, mgr, prison_no)"
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
