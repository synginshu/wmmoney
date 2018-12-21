class Account:
    def __init__(self, AcctID, Type, Name, Currency, StartingBalance, Notes):
        self.AcctID = AcctID
        self.Type = Type
        self.Name = Name
        self.Currency = Currency
        self.StartingBalance = StartingBalance
        self.Notes = Notes

    # Save in database
    def create(self,db):
        print ('todo')
        sql = "INSERT INTO tbl_account (Type,Name,Currency,StartingBalance,Notes) VALUES ('%s','%s','%s',%d,'%s')" % (self.Type, self.Name, self.Currency, self.StartingBalance, self.Notes)        
        print (sql)
        db.execute(sql)


    def toString(self):
        return (self.Type, self.Name, self.Currency, self.StartingBalance)
