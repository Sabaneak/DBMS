from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple


class Prison(Resource):
    @jwt_required()
    def get(self, pno):
        sql = "SELECT * FROM prisond LEFT JOIN prisond1 USING (pno) LEFT JOIN prisond2 USING (pno) LEFT JOIN prisond3 USING (pno) LEFT JOIN prisond4 USING (pno) WHERE pno = %s"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prison does not exist'}, 400
        else:
            return {'Prison {}'.format(pno): res}, 200

    @jwt_required()
    def post(self, pno):
        body = request.get_json()
        sql = "INSERT INTO prison (pno, capacity, district, city) VALUES (%s, %s, %s, %s)"
        tuple = (pno, body['capacity'], body['district'], body['city'])

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Prison added'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self, pno):
        sql = "DELETE FROM prison WHERE pno = %s"
        tuple = (pno)

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Prison deleted'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400

class Prisons_All(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT pr.pno, pr.capacity, pr.district, pr.city, count(p.pid) AS prisoner_count FROM prison pr LEFT JOIN prisoner p on p.prison_no = pr.pno GROUP BY p.prison_no, pr.pno, pr.capacity, pr.district, pr.city"
        sql1 = "SELECT * FROM prisond5, prisond6"
        res = execute_sql(sql=sql)
        res1 = execute_sql(sql=sql1)
        if res == "[]":
            return {'msg': 'Prison does not exist'}, 400
        else:
            return {'Prisons': res, 'Total': res1}, 200