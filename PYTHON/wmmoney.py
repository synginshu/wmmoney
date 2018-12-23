#!/usr/bin/python

import sys
import Logging as logging
from tokenize import tokenize
from Account import Account, AccountController
from Categories import Category, CategoryController
from Tag import Tag, TagController
from Transaction import Transaction, TransactionController
from Portfolio import Portfolio, PortfolioController
from Query import QueryController


from MoneyDB import MoneyDB

import sys, getopt

def main(argv):
	logging.setoutput(sys.stdout)

	if len(argv) >= 1 and argv[0] == 'interactive':
		interactive()
	else:
		process(argv)

def interactive():
	global quit

	logging.logOutput ('Entering interactive mode')
	while not quit:
		command = input('Money> ')
		process(command.split())

def process(argv):
	global quit
	global db
	didSomething = False

	msg = ('Processing: ' , argv[0:])
	logging.logDebug (msg)
	if argv[0] == 'quit':
		quit = True
		didSomething = True

	# All account stuff
	if argv[0].startswith('a'):
		logging.logDebug ('Account')
		ac = AccountController()
		didSomething = ac.process(argv,db)

	# All category stuff
	if argv[0].startswith('c'):
		logging.logDebug ('Categories')
		cc = CategoryController()
		didSomething = cc.process(argv,db)

	# All tag stuff
	if argv[0].startswith('g'):
		logging.logDebug ('Tags')
		tagC = TagController()
		didSomething = tagC.process(argv,db)

	# All transaction stuff
	if argv[0].startswith('t'):
		logging.logDebug ('Transactions')
		tc = TransactionController()
		didSomething = tc.process(argv,db)

	# All portfolio stuff
	if argv[0].startswith('p'):
		logging.logDebug ('Portfolio')
		pc = PortfolioController()
		didSomething = pc.process(argv,db)

	# All query stuff
	if argv[0].startswith('q'):
		logging.logDebug ('Query')
		qc = QueryController()
		didSomething = qc.process(argv,db)

	# log the command if we did something
	if didSomething:
		command = " ".join(str(x) for x in argv)
		logging.logCommand(command)

	if didSomething == False or argv[0] == 'help':
		logging.output ("List of commands\n ca - create account\n quit - Quit")

# Initialize the quit flag
quit = False

# load the DB
db = MoneyDB()

if __name__ == "__main__":
   main(sys.argv[1:])

