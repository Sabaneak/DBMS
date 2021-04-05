from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple

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