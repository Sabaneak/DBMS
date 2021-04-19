from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple


class Business(Resource):
    @jwt_required()
    def get(self, bus_id):
        sql = "SELECT bid, bname, role, role_desc, sal, number_required FROM business where bid=%s"
        tuple = (bus_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Business does not exist'}, 400
        else:
            return {'Business {}'.format(bus_id): res}, 200

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
        try:
            sql_1 = "UPDATE prisoners SET employed_by=NULL where employed_by=%s"
            tuple_1 = bus_id
            res_1 = execute_sql_tuple(sql_1, tuple_1)

            sql_2 = "DELETE FROM business WHERE bid = %s"
            tuple_2 = (bus_id)
            res_2 = execute_sql_tuple(sql_2, tuple_2)
            return {'msg': 'Business deleted'}, 200

        except Exception as e:
            return {'msg': str(e)}, 400

class EmpBidComb(Resource):
    @jwt_required()
    def get(self,pno):
        sql="select employed_by,bid from prisoner,business where pid=%s"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Combination Not Found'}, 400
        else:
            return {'Combination {}'.format(pno): res}, 200

class updateBusID(Resource):
    @jwt_required()
    def put(self):
        body = request.get_json()
        sql="update prisoner set employed_by=%s where pid=%s"
        tuple=(body['bid'],body['pid'])
        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Update Done!'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400
