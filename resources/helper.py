from db import db
import simplejson
import pymysql

def execute_sql(sql):
    curs = db.cursor(pymysql.cursors.DictCursor)
    curs.execute(sql)
    results = curs.fetchall()
    db.commit()
    curs.close()
    return simplejson.dumps(results)

def execute_sql_tuple(sql, tuple):
    curs = db.cursor(pymysql.cursors.DictCursor)
    curs.execute(sql, tuple)
    results = curs.fetchall()
    db.commit()
    curs.close()
    return simplejson.dumps(results)
