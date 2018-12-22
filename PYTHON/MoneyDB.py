import sqlite3

class MoneyDB:
	def __init__(self):
		self.conn = sqlite3.connect('../DATABASE/wmm.db')


	def insertpk(self,sql,params):
		c = self.conn.cursor()
		c.execute(sql,params)
		self.conn.commit()
		return c.lastrowid

	def execute(self,sql,params):
		c = self.conn.cursor()
		c.execute(sql,params)
		self.conn.commit()
		return c.rowcount

	def query(self, sql,params):
		c = self.conn.cursor()
		c.execute(sql,params)
		row = c.fetchone()
		return row

	def list(self, sql,params):
		c = self.conn.cursor()
		c.execute(sql,params)
		rows = c.fetchall()
		return rows

	def exit(self):
		self.conn.close();


