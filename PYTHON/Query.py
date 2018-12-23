import Logging as logging

class QueryController:
	def process(self,argv,db):
		if argv[0] == 'qa':
			return self.queryAccountNo(argv,db)

	def queryAccountNo(self,argv,db):
		logging.logDebug ("Query Account ID " + argv[1] + argv[2])
		try:
			if len(argv) >= 2:
				sql = "SELECT AcctID From tbl_Account WHERE Bank = ? and AccountNo = ?"
				params = (argv[1],argv[2])
				result = db.query(sql,params)
				logging.output(str(result[0]))
				return True

		except Exception as e:
			logging.logException (e)
			return False
		return True
