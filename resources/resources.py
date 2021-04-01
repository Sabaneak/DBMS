from flask_restful import Resource
from .helper import execute_sql

class Prisoner(Resource):
    def get(self):
        sql = "SELECT * FROM prisoner"
        res = execute_sql(sql=sql)
        return {'Prisoners': res}, 200

