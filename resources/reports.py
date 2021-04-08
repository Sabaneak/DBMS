from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .helper import execute_sql, execute_sql_tuple

class PrisonerReport(Resource):
    @jwt_required()
    def get(self, pid):
        sql = "SELECT p.pid, p.prison_no, p.first_name, p.last_name, p.age, c.c_name, sum(c.c_years), p.ht_in_m, p.wt_in_kg, p.eye_colour, p.hair_colour, p.fingerprint, pi.identifying_mark, pa.p_2, p.entry_date, p.visits_made, p.employed_by, pc.chore_name, ch.chore_time, r.first_name, r.last_name, r.relation FROM prisoner p LEFT JOIN prisoner_id_marks pi ON pi.pid = p.pid LEFT JOIN prisoner_affiliations pa ON pa.p_1 = p.pid LEFT JOIN prisoner_chores pc ON pc.pid = p.pid LEFT JOIN chore ch ON ch.chore_name = pc.chore_name LEFT JOIN relative r ON r.pid = p.pid LEFT JOIN crime_records cr ON p.pid = cr.pid LEFT JOIN crime c ON cr.cid = c.cid WHERE p.pid = %s"
        tuple = (pid)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prisoner does not exist'}, 400
        else:
            return {'Prisoner {}'.format(pid): res}, 200

class GuardReport(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT s.empid, prison_no, first_name, last_name, salary, years_of_experience, mgr, shift_number FROM official o, guard_shifts s WHERE o.empid = %s AND o.empid = s.empid AND type = 'Guard'"
        tuple = (_id)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Guard does not exist'}, 400
        else:
            return {'Guard {}'.format(_id): res}, 200

class WardenReport(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT e1.empid, e1.prison_no, e1.first_name, e1.last_name, e1.salary, e1.years_of_experience, (SELECT count(*) FROM official e2 WHERE e2.mgr = e1.empid) AS employees FROM official e1 WHERE e1.type = 'Warden' AND e1.empid = %s"
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
        sql = "SELECT pr.pno, pr.capacity, pr.district, pr.city, pf.facility_name, SUM(pf.count*pf.cost_per_unit_monthly) AS maintenance_cost, (SELECT SUM(salary) FROM official o WHERE o.prison_no = pr.pno) AS employee_salaries, (SELECT COUNT(*) FROM official o WHERE o.prison_no = pr.pno) AS workforce FROM prison pr, prison_facilities pf WHERE pf.prison_no = pr.pno GROUP BY pr.pno HAVING pr.pno = %s"
        tuple = (pno)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Chores do not exist'}, 400
        else:
            return {'Chore {}'.format(pno): res}, 200

class ChiefWardenReport(Resource):
    @jwt_required()
    def get(self, _id):
        sql = "SELECT e1.empid, e1.prison_no, e1.first_name, e1.last_name, e1.salary, e1.years_of_experience, (SELECT count(*) FROM official e2 WHERE e2.mgr = e1.empid) AS employees FROM official e1 WHERE e1.type = 'Chief Warden' AND e1.empid = %s"
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
        sql = "SELECT p.pid, p.first_name, p.last_name, c.c_name FROM prisoner p, crime c, crime_records cr WHERE p.pid = cr.pid AND cr.cid = c.cid AND p.prison_no = %s"
        tuple = (prison_no)
        res = execute_sql_tuple(sql=sql, tuple=tuple)

        if res == "[]":
            return {'msg': 'Prisoner not found'}, 400
        else:
            return {'Prisoner {}'.format(prison_no): res}, 200

