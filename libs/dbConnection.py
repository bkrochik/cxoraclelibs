import cx_Oracle

def getDBCursor(ip,port,sid,user,pwd):
	#Setting connection TNS
    dsn_tns = cx_Oracle.makedsn(ip, port, sid)
    return cx_Oracle.connect(user,pwd, dsn_tns)
    