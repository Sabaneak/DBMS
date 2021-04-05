from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple

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