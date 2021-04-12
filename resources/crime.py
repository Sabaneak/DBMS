from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple


class Crime(Resource):
    @jwt_required()
    def get(self, cid):
        sql = "SELECT * FROM crime where cid=%s"
        tuple = (cid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Crime does not exist'}, 400
        else:
            return {'Prison {}'.format(cid): res}, 200

    @jwt_required()
    def post(self, cid):
        body = request.get_json()
        sql = "INSERT INTO crime (cid, c_name, c_desc, c_years) VALUES (%s, %s, %s, %s)"
        tuple = (cid, body['c_name'], body['c_desc'], body['c_years'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Crime added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

class Crime_Records(Resource):
    @jwt_required()
    def post(self, pid):
        body = request.get_json()
        sql = "INSERT INTO crime_records (pid, cid) VALUES (%s, %s)"
        tuple = (pid, body['cid'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Crime added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

