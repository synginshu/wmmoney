#!/usr/bin/python

import sys
from tokenize import tokenize
from Account import Account, AccountController

from MoneyDB import MoneyDB

import sys, getopt

def main(argv):
	if len(argv) >= 1 and argv[0] == 'interactive':
		interactive()
	else:
		process(argv)

def interactive():
	global quit

	print ('Entering interactive mode')
	while not quit:
		command = input('Money> ')
		process(command.split())

def process(argv):
	global quit
	global db
	didSomething = False

	print ('Processing:' , argv[0:])
	if argv[0] == 'quit':
		quit = True
		didSomething = True

	# Create account
	if argv[0] == 'ca':
		ac = AccountController()
		didSomething = ac.createAccount(argv,db)

	if didSomething == False or argv[0] == 'help':
		print ("List of commands\n ca - create account\n quit - Quit")

# Initialize the quit flag
quit = False

# load the DB
db = MoneyDB()

if __name__ == "__main__":
   main(sys.argv[1:])

