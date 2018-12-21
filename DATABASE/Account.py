class Account:
	def __init__(self, AcctID, Type, Name, StartingBalance, Currency, StartingBalance, Notes):
		self.AcctID = AcctID
	    self.Type = Type
    	self.Name = Name
    	self.Currency = Currency
    	self.StartingBalance = StartingBalance
    	self.Notes = Notes

    # Save in database
    def create(self):
    	#todo

    def toString(self):
    	print (self.Type, self.Name, self.Currency, self.StartingBalance)
