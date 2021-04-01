from db import db
import simplejson

def execute_sql(sql):
    curs = db.cursor()
    curs.execute(sql)
    results = curs.fetchall()
    db.commit()
    curs.close()
    return simplejson.dumps(results)