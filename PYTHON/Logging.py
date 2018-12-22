import traceback

def logDebug(message):
	print ("DEBUG: " + str(message))

def logException(e):
	print ("Exception: " + str(e))
	print (traceback.format_exc())

def logSQL(sql):
	print ("SQL: " + sql)

def output(message):
	print ("OUTPUT: " + message)
