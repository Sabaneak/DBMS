from db import db
import simplejson

def execute_sql(sql):
    curs = db.cursor()
    curs.execute(sql)
    results = curs.fetchall()
    db.commit()
    curs.close()
    return simplejson.dumps(results)

def execute_sql_tuple(sql, tuple):
    curs = db.cursor()
    curs.execute(sql, tuple)
    results = curs.fetchall()
    db.commit()
    curs.close()
    return simplejson.dumps(results)
