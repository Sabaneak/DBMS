from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple

class Facility(Resource):
    @jwt_required()
    def get(self, pno):
        sql = "SELECT * FROM prison_facilities WHERE prison_no = %s"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prison does not exist'}, 400
        else:
            return {'Prison {}'.format(pno): res}, 200

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
        tuple = (pno, body['facility_name'])

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