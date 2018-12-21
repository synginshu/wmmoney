import sqlite3

class MoneyDB:
	def __init__(self):
		self.conn = sqlite3.connect('../DATABASE/wmm.db')

	def execute(self,sql):
		c = self.conn.cursor()
		c.execute(sql)
		self.conn.commit();

	def exit(self):
		self.conn.close();


