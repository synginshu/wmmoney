import traceback
import datetime
import sys

global outputStream

def logDebug(message):
	print ("DEBUG: " + str(message))

def logException(e):
	print ("Exception: " + str(e))
	print (traceback.format_exc())

def logSQL(sql):
	print ("SQL: " + sql)

def setoutput(stream):
	global outputStream
	outputStream = stream

def output(message):
	outputStream.write("OUTPUT: " + message + '\n')
	outputStream.flush()

def logCommand(message):
	filename = "commandLog.log"
	f= open(filename,"a+")
	f.write (str(datetime.date.today()) + " : " + message)
	f.close
