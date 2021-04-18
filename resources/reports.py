from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple

class PrisonerReport(Resource):
    @jwt_required()
    def get(self, pid):
        sql = "SELECT * FROM prisonerd LEFT JOIN prisonerd1 USING (pid) LEFT JOIN prisonerd2 USING (pid) LEFT JOIN prisonerd3 USING (pid) LEFT JOIN prisonerd4 USING (pid) LEFT JOIN prisonerd5 USING (pid) LEFT JOIN prisonerd6 USING (pid) WHERE pid = %s"
        tuple = (pid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prisoner does not exist'}, 400
        else:
            return {'Prisoner {}'.format(pid): res}, 200

class GuardReport(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT o.empid, o.prison_no, district, city, o.first_name, o.last_name, o.salary, o.years_of_experience, o.mgr, o1.first_name as mgr_first_name, o1.last_name as mgr_last_name, shift_number FROM official o LEFT JOIN prison pr on o.prison_no = pr.pno LEFT JOIN official o1 on o1.empid = o.mgr LEFT JOIN guard_shifts s on o.empid = s.empid WHERE o.empid = %s AND o.type = 'Guard'"
        tuple = (_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Guard does not exist'}, 400
        else:
            return {'Guard {}'.format(_id): res}, 200

class WardenReport(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT o.empid, o.prison_no, district, city, o.first_name, o.last_name, o.salary, o.years_of_experience, o.mgr, o1.first_name as mgr_first_name, o1.last_name as mgr_last_name, count(o2.empid) as employees FROM official o LEFT JOIN prison pr on o.prison_no = pr.pno LEFT JOIN official o1 on o1.empid = o.mgr LEFT JOIN official o2 on o2.mgr = o.empid WHERE o.type = 'Warden' AND o.empid = %s"
        tuple = (_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Warden does not exist'}, 400
        else:
            return {'Warden {}'.format(_id): res}, 200

class PrisonReport(Resource):
    @jwt_required()
    def get(self, pno):
        sql = "SELECT s.empid, prison_no, first_name, last_name, salary, years_of_experience, mgr, shift_number FROM official o, guard_shifts s WHERE o.empid = %s AND o.empid = s.empid AND type = 'Guard'"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prison does not exist'}, 400
        else:
            return {'Prison {}'.format(pno): res}, 200

class ChoreSheet(Resource):
    @jwt_required()
    def get(self, pno):
        sql = "SELECT c.pid, c.chore_name, c1.chore_time FROM prisoner_chores c, chore c1 WHERE c.prison_no = c1.prison_no AND c.chore_name = c1.chore_name AND prison_no = %s"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Chores do not exist'}, 400
        else:
            return {'Chore {}'.format(pno): res}, 200

class ChiefWardenReport(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT o.empid, o.prison_no, district, city, o.first_name, o.last_name, o.salary, o.years_of_experience, o.mgr, o1.first_name as mgr_first_name, o1.last_name as mgr_last_name, count(o2.empid) as employees FROM official o LEFT JOIN prison pr on o.prison_no = pr.pno LEFT JOIN official o1 on o1.empid = o.mgr LEFT JOIN official o2 on o2.mgr = o.empid WHERE o.type = 'Chief Warden' AND o.empid = %s"
        tuple = (_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)
        if res == "[]":
            return {'msg': 'Chief Warden does not exist'}, 400
        else:
            return {'Chief Warden {}'.format(_id): res}, 200


class RelativeSheet(Resource):
    @jwt_required()
    def get(self, rid):
        sql = "SELECT r.rid, r.first_name, r.last_name, r.pid, r.relation, p.prison_no, v.appointment_date FROM relative r, visit v, prisoner p WHERE v.rid = r.rid AND r.pid = p.pid AND r.rid = %s"
        tuple = (rid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Relative does not exist'}, 400
        else:
            return {'Relative {}'.format(rid): res}, 200


class BusinessSheet(Resource):
    @jwt_required()
    def get(self, bid):
        sql = "SELECT bid, bname, role, role_desc, sal, number_required, count(pid) AS number_employed FROM business, prisoner GROUP BY employed_by, bid, bname, role, role_desc, sal, number_required HAVING employed_by = bid AND bid = %s"
        tuple = (bid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Business does not exist'}, 400
        else:
            return {'Business {}'.format(bid): res}, 200


class BusinessAll(Resource):
    @jwt_required()
    def get(self):
        sql = "SELECT bid, bname, role, role_desc, sal, number_required, count(pid) AS number_employed FROM business, prisoner GROUP BY employed_by, bid, bname, role, role_desc, sal, number_required HAVING employed_by = bid"
        res = execute_sql(sql=sql)
        if res == "[]":
            return {'msg': 'Business does not exist'}, 400
        else:
            return {'Business {}'.format(100): res}, 200

class VisitSheet(Resource):
    @jwt_required()
    def get(self, prison_no):
        sql = "SELECT v.vid, v.rid, r.pid, r.first_name, r.last_name, r.relation FROM visit v, relative r, prisoner p WHERE v.rid = r.rid AND r.pid = p.pid AND p.prison_no = %s"
        tuple = (prison_no)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Visit not made'}, 400
        else:
            return {'Visit {}'.format(prison_no): res}, 200


class PrisonerPrison(Resource):
    @jwt_required()
    def get(self, prison_no):
        sql = "SELECT p.pid, p.first_name, p.last_name FROM prisoner p WHERE p.prison_no = %s"
        tuple = (prison_no)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prisoner not found'}, 400
        else:
            return {'Prison {}'.format(prison_no): res}, 200

class PrisonerBusiness(Resource):
    @jwt_required()
    def get(self, bid):
        sql = "SELECT p.pid, p.first_name, p.last_name FROM prisoner p WHERE p.employed_by = %s"
        tuple = (bid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prisoner not found'}, 400
        else:
            return {'Business {}'.format(bid): res}, 200

class GuardWarden(Resource):
    @jwt_required()
    def get(self, empid):
        sql = "SELECT o.empid, o.first_name, o.last_name FROM official o WHERE o.mgr = %s"
        tuple = (empid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Guard not found'}, 400
        else:
            return {'Warden {}'.format(empid): res}, 200

class GuardChiefWarden(Resource):
    @jwt_required()
    def get(self, pno):
        sql = "SELECT o.empid, o.first_name, o.last_name FROM official o WHERE o.prison_no = %s AND o.type='Guard'"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Guard not found'}, 400
        else:
            return {'Prison {}'.format(pno): res}, 200

class WardenChiefWarden(Resource):
    @jwt_required()
    def get(self, empid):
        sql = "SELECT o1.empid, o.prison_no, p.district, p.city FROM official o, official o1, prison p WHERE o1.mgr = o.empid AND o.prison_no = p.pno AND o1.type = 'Warden' AND o.empid = %s"
        tuple = (empid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Wardens not found'}, 400
        else:
            return {'Chief Warden {}'.format(empid): res}, 200

class BusinessRequirement(Resource):
    @jwt_required()
    def get(self,bid):
        sql="select B.bid,B.bname,B.number_required,count(*) as currently_employed from business B,prisoner P where P.employed_by=B.bid group by B.bid,B.bname,B.number_required AND B.bid=%s"
        tuple = (bid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)
        
        if res == "[]":
            return {'msg': 'Wardens not found'}, 400
        else:
            return {'Business Requirments {}'.format(bid): res}, 200

class UpdateRequirement(Resource):
    @jwt_required()
    def put(self,bid):
        body = request.get_json()
        sql="UPDATE BUSINESS SET number_required= %s where bid=%s"
        tuple=(body['new_requirement'],bid)
        try:
            res = execute_sql_tuple(sql=sql, tuple=tuple)
            return {'msg': 'Business Requirement updated'}, 200
        except Exception as e:
            return {'msg': str(e)}, 400



