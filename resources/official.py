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
        try:
            sql_1 = "UPDATE official SET mgr=200001 WHERE mgr=%s"
            tuple_1 = empid
            res_1 = execute_sql_tuple(sql_1, tuple_1)

            sql_3 = "DELETE FROM guard_shifts WHERE empid=%s"
            tuple_3 = empid
            res_3 = execute_sql_tuple(sql_3, tuple_3)

            sql_2 = "DELETE FROM official WHERE empid = %s"
            tuple_2 = (empid)
            res_2 = execute_sql_tuple(sql_2, tuple_2)

            return {'msg': 'Official deleted'}, 200

        except Exception as e:
            return {'msg': str(e)}, 400

class Wardens(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT empid, first_name, last_name, prison_no FROM official WHERE type = 'Warden'"
        res = execute_sql(sql=sql)

        if res == "[]":
            return {'msg': 'No wardens'}, 400
        else:
            return {'Wardens': res}, 200

class Guards(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT empid, first_name, last_name, prison_no FROM official WHERE type = 'Guard'"
        res = execute_sql(sql=sql)

        if res == "[]":
            return {'msg': 'No guards'}, 400
        else:
            return {'Guards': res}, 200

class ChiefWardens(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT empid, prison_no FROM official WHERE type = 'Chief Warden'"
        res = execute_sql(sql=sql)

        if res == "[]":
            return {'msg': 'No chief wardens'}, 400
        else:
            return {'Chief Wardens': res}, 200

class GuardWardenComb(Resource):
    @jwt_required()
    def get(self,empid):
        sql="select G.mgr,M.empid as cempid from official G,official M where G.empid=%s and M.type='Warden' and M.prison_no = G.prison_no"
        tuple = (empid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Combination Not Found'}, 400
        else:
            return {'Combination {}'.format(empid): res}, 200

class UpdateMgrID(Resource):
    @jwt_required()
    def put(self):
        body = request.get_json()
        sql="update official set mgr=%s where empid=%s"
        tuple=(body['cempid'],body['empid'])
        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Update Done!'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400
