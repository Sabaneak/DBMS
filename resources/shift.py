from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple

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