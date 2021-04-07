from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple


class Business(Resource):
    @jwt_required()
    def get(self, bus_id):
        sql = "SELECT bid, bname, role, role_desc, sal, number_required FROM business where bid=bus_id and bus_id=%s"
        tuple = (bus_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Business does not exist'}, 400
        else:
            return {'Business {}'.format(bid): res}, 200

    @jwt_required()
    def post(self, bus_id):
        body = request.get_json()
        sql = "INSERT INTO business (bid, password, bname, role, role_desc, sal, number_required) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        tuple = (bus_id, body['password'], body['bname'], body['role'], body['role_desc'], body['sal'],
                 body['number_required'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Business added'}, 200

        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self, bus_id):
        sql = "DELETE FROM business WHERE bid = %s"
        tuple = (bid)

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Business deleted'}, 200

        except Exception as e:
            return {'msg': str(e)}, 400

