from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from .helper import execute_sql, execute_sql_tuple
from blacklist import BLACKLIST

class Prisoner_Login(Resource):
    def post(self):
        body = request.get_json()
        sql = "SELECT * FROM prisoner where pid=%s and password=%s"
        tuple = (body['pid'], body['password'])
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'No such prisoner exists. Recheck credentials'}, 400
        else:
            access_token = create_access_token(identity=str(body['pid']), fresh=True)

        return {'access_token': access_token}, 200

class Official_Login(Resource):
    def post(self):
        body = request.get_json()
        sql = "SELECT * FROM official where empid=%s and password=%s"
        tuple = (body['empid'], body['password'])
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'No such official exists. Recheck credentials'}, 400
        else:
            access_token = create_access_token(identity=str(body['empid']), fresh=True)

        return {'access_token': access_token}, 200

class Business_Login(Resource):
    def post(self):
        body = request.get_json()
        sql = "SELECT * FROM business where bid=%s and password=%s"
        tuple = (body['bid'], body['password'])
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'No such business exists. Recheck credentials'}, 400
        else:
            access_token = create_access_token(identity=str(body['bid']), fresh=True)

        return {'access_token': access_token}, 200

class Relative_Login(Resource):
    def post(self):
        body = request.get_json()
        sql = "SELECT * FROM relative where rid=%s and password=%s"
        tuple = (body['rid'], body['password'])
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'No such relative exists. Recheck credentials'}, 400
        else:
            access_token = create_access_token(identity=str(body['rid']), fresh=True)

        return {'access_token': access_token}, 200

class User_Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'msg': 'User has been logged out'}, 200