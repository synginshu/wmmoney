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
        sql = "INSERT INTO tbl_account (Type,Name,Currency,StartingBalance,Notes) VALUES (%s,'%s','%s',%s,'%s')" % (self.Type, self.Name, self.Currency, self.StartingBalance, self.Notes)        
        print (sql)
        db.execute(sql)


    def toString(self):
        return (self.Type, self.Name, self.Currency, self.StartingBalance)


class AccountController:
    def createAccount(self,argv,db):
        try:
            if len(argv) == 5:
                a = Account('AcctID',argv[1],argv[2],argv[3],argv[4],'')

            if len(argv) == 6:
                a = Account('AcctID',argv[1],argv[2],argv[3],argv[4],argv[5])
            a.create(db)     
        except Exception as valerr:
            print (valerr)
        except:
            # print help
            print ("ca [Type: 1|2] [Name] [Currency MYR|USD] [Starting Balance] [Notes]")

        return True;