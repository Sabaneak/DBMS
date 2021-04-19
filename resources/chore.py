from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple

class Chore(Resource):
    @jwt_required()
    def post(self):
        body = request.get_json()
        sql = "INSERT INTO prisoner_chores (pid, prison_no, chore_name) VALUES (%s, %s, %s)"
        tuple = (body['pid'], body['prison_no'], body['chore_name'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Chore added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self):
        body = request.get_json()
        sql = "DELETE FROM prisoner_chores WHERE pid = %s AND prison_no = %s AND chore_name = %s"
        tuple = (body['pid'], body['prison_no'], body['chore_name'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Chore deleted'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

class ChorePrison(Resource):
    @jwt_required()
    def get(self, pno):
        sql = "SELECT * FROM chore WHERE prison_no = %s"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Chores do not exist'}, 400
        else:
            return {'Chore {}'.format(pno): res}, 200
    
    @jwt_required()
    def post(self, pno):
        body = request.get_json()
        sql = "INSERT INTO chore (prison_no, chore_name, people_needed, chore_time) VALUES (%s, %s, %s, %s)"
        tuple = (pno, body['chore_name'], body['people_needed'], body['chore_time'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Chore added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

class ChorePrisoner(Resource):
    @jwt_required()
    def get(self, pno):
        sql = "SELECT p.pid, c.chore_name FROM prisoner p, chore c WHERE p.prison_no = c.prison_no AND p.prison_no = %s"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Chores do not exist'}, 400
        else:
            return {'Prison {}'.format(pno): res}, 200