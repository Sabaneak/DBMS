from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple


class Prisoner(Resource):
    @jwt_required()
    def post(self, pid):
        body = request.get_json()

        try:
            #Prisoner table
            sql_1 = "INSERT INTO prisoner (pid, password, first_name, last_name, age, ht_in_m, wt_in_kg, eye_colour, " \
                  "hair_colour, fingerprint, visits_made, prison_no, employed_by, entry_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            tuple_1 = (
            pid, body['password'], body['first_name'], body['last_name'], body['age'], body['ht_in_m'], body['wt_in_kg'], body['eye_colour'],
            body['hair_colour'], body['fingerprint'], body['visits_made'], body['prison_no'], body['employed_by'], body['entry_date'])
            res_1 = execute_sql_tuple(sql=sql_1, tuple=tuple_1)

            #Prisoner_Crimes
            sql_2 = "INSERT INTO crime_records (pid, cid) VALUES (%s, %s)"
            for i in range(len(body['cid'])):
                tuple_2 = (pid, body['cid'][i])
                res_2 = execute_sql_tuple(sql=sql_2, tuple=tuple_2)

            #Prisoner_Affiliations
            sql_3 = "INSERT INTO prisoner_affiliations (p_1, p_2) VALUES (%s, %s)"
            for i in range(len(body['pid'])):
                tuple_3 = (pid, body['pid'][i])
                res_3 = execute_sql_tuple(sql=sql_3,tuple=tuple_3)

            #Prisoner_ID
            sql_4 = "INSERT INTO prisoner_id_marks (pid, identifying_mark) VALUES (%s, %s)"
            for i in range(len(body['identifying_mark'])):
                tuple_4 = (pid, body['identifying_mark'][i])
                res_4 = execute_sql_tuple(sql=sql_4, tuple=tuple_4)

            return {'msg': 'Prisoner added'}, 200

        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def delete(self, pid):

        try:
            #Prisoner_ID
            sql_1 = "DELETE FROM prisoner_id_marks WHERE pid = %s"
            tuple_1 = (pid)
            res = execute_sql_tuple(sql=sql_1, tuple=tuple_1)

            #Prisoner_Affiliations
            sql_2 = "DELETE FROM prisoner_affiliations WHERE pid = %s"
            tuple_2 = (pid)
            res = execute_sql_tuple(sql=sql_2, tuple=tuple_2)

            #Prisoner_Crimes
            sql_3 = "DELETE FROM crime_records WHERE pid = %s"
            tuple_3 = (pid)
            res = execute_sql_tuple(sql=sql_3, tuple=tuple_3)

            sql_4 = "DELETE FROM prisoner WHERE pid = %s"
            tuple_4 = (pid)
            res = execute_sql_tuple(sql=sql_4, tuple=tuple_4)

            return {'msg': 'Prisoner deleted'}, 200

        except Exception as e:
            return {'msg': str(e)}, 400

    @jwt_required()
    def put(self, pid):
        body = request.get_json()
        sql = "UPDATE prisoner SET prison_no = %s WHERE pid = %s"
        tuple = (body['pno'], pid)

        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Prisoner {} shifted to prison {}'.format(pid, body['pno'])}, 200
        except Exception as e:
            return {'msg': str(e)}, 400


class Prisoners(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT p.pid, p.first_name, p.last_name, c.c_name FROM prisoner p, crime c, crime_records cr WHERE p.pid = cr.pid AND cr.cid = c.cid ORDER BY p.pid"
        res = execute_sql(sql=sql)

        if res == "[]":
            return {'msg': 'No prisoners'}, 400
        else:
            return {'Prisoners': res}, 200


class AddPrisonerComponents(Resource):
    @jwt_required()
    def get(self, pno):
        body = request.get_json()
        sql = "SELECT cr.cid, cr.c_name, pr.pid FROM crime cr JOIN prisoner pr LEFT JOIN prison p ON pr.prison_no = p.pno WHERE p.pno = %s"
        tuple = (pno)
        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'Prison {}'.format(pno): res}, 200
        except Exception as e:
            return {'msg': str(e)}, 400
