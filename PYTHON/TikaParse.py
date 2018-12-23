#!/usr/bin/env python
import io
import tika
import re
from tika import parser
import Logging as logging
from wmmoney import process
import datetime
import csv
import sys

global map
map = {
  "TPE": ("EXP", "INVEST", "BUY", "pc" ),
  "TRA": ("TRF", "BANK", "TRANSFER", "tc"),
  "DV/": ("INC", "BANK", "DIVIDEND", "tc"),
  "INT": ("INC", "BANK", "INTEREST", "tc")  
}


def readMap():
	global map
	reader = csv.reader(open('../Sample PDF/MBBCombine.csv', 'r'))
	map = {}
	for row in reader:
		map[row[0]] = row[1:]
	print(map)

def callWMM(command):
	output = io.StringIO()
	logging.setoutput(output)
	process (command)
	return output.getvalue()


def postTransaction(line,bank,acct):
	# find acctID for number
	global map

	command = ('qa' , bank, acct)
	result = callWMM(command)
	acctID = result.split()[1]

	# parse the transaction
	tokens = line.split()

	#Get the date
	curYear = str(datetime.date.today().year)
	tDate = datetime.datetime.strptime( tokens[0]+curYear, "%d%b%Y" )

	# Get the amount
	amountIndex = len(tokens) - 2
	tAmount = (tokens[amountIndex])

	# Get the main body
	key = tokens[2][0:3]
	if key in map:
		value = map[key]
		tType = value[0]
		tL1 = value[1]
		tL2 = value[2]
		tCommand = value[3]
		if tCommand == "pc":
			# more
			tSC = tokens[3]
			splitIndex = tokens[4].find("@")
			tUnits = tokens[4][0:splitIndex]
			tPrice = tokens[4][splitIndex+1:]

	else:
		tType = 'EXP'
		tL1 = ''
		tL2 = ''
		tCommand = 'tc'

	tCur = 'MYR'
	# Portfolio
	if tCommand == "pc":
		command = (tCommand , '0', tType, tL1, tL2, acctID, tCur, tAmount, tDate, "", "", tSC, tUnits, tPrice, '0')

	# Transaction
	if tCommand == "tc":
		command = (tCommand , '0', tType, tL1, tL2, acctID, tCur, tAmount, tDate, "", "")

	print(command)
	result = callWMM(command)
	print(result)


#Read the map for parsing
readMap()

#tika.initVM()
raw = parser.from_file(sys.argv[1])

content = raw['content']
#print(raw['content'])

# find Your Banking Account Activities / Urusniaga Akaun Anda
lastIndex = 0
target = "Your Banking Account Activities / Urusniaga Akaun Anda"
newIndex = content.find(target,lastIndex)

target = "Your Investment Portfolio / Senarai Pelaburan Anda"
lastIndex = content.find(target,newIndex)

#Extract the section
section = content[newIndex:lastIndex]

#split into lines
lines = section.splitlines()
inAccount = False;
for line in lines:

	if re.search('[0-9]{12}$',line) and not inAccount:
		#Get a/c no - last token of the line
		tokens = line.split();
		print (tokens)
		acctNo = tokens[len(tokens) - 1]
		inAccount = True
		print ("Found account: " + acctNo)

	# check if first 5 chars of line is a date format ddMMM
	if re.match('^(0[1-9]|[12][0-9]|3[01])',line) and inAccount:
		print ("Found a transaction: " + line)
		postTransaction(line, "MBB",acctNo)

	if line.find("CLOSING BALANCE") >= 0 and inAccount:
		inAccount = False
		print ("Leaving account: " + acctNo)









