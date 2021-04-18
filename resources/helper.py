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

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)