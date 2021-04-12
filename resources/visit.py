from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple
import json
from datetime import *

class Visit(Resource):
    @jwt_required()
    def post(self):
        body = request.get_json()

        temp_sql = "SELECT appointment_date FROM visit, relative, prisoner WHERE visit.rid = relative.rid AND relative.pid = prisoner.pid AND relative.rid = %s ORDER BY appointment_date LIMIT 1"
        temp_tuple = body['rid']
        temp = execute_sql_tuple(sql=temp_sql, tuple=temp_tuple)

        app_date = json.loads(temp)[0]['appointment_date']
        dur = datetime.strptime(body['appointment_date'], '%Y-%m-%d') - datetime.strptime(str(app_date), '%Y-%m-%d')

        if dur.days < 14:
            return {'msg': 'Visits must have at least 2 weeks between them'}, 400

        else:
            try:
                sql = "INSERT INTO visit (vid, rid, appointment_date) VALUES (%s, %s, %s)"
                tuple = (body['vid'], body['rid'], body['appointment_date'])
                res = execute_sql_tuple(sql=sql, tuple=tuple)
                return {'msg': 'Visit added'}, 200

            except Exception as e:
                return {'msg': str(e)}, 400
