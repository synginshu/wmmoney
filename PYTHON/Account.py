import Logging as logging
class Account:

    def __init__(self, AcctID, Type, Name, Bank, AccountNo, Currency, StartingBalance, Notes):
        self.AcctID = AcctID
        self.Type = Type
        self.Name = Name
        self.Bank = Bank
        self.AccountNo = AccountNo
        self.Currency = Currency
        self.StartingBalance = StartingBalance
        self.Notes = Notes

    # Save in database
    def create(self,db):
        sql = "INSERT INTO tbl_account (Type,Name,Bank,AccountNo,Currency,StartingBalance,Notes) VALUES (?,?,?,?,?,?,?)" 
        params = (self.Type, self.Name, self.Bank, self.AccountNo, self.Currency, self.StartingBalance, self.Notes)        
        # logging.logSQL (sql,params)
        db.execute(sql,params)

    def update(self,db):
        sql = "UPDATE tbl_account Set Type = ?, Name = ?, Bank = ?, AccountNo = ?, Currency = ?, StartingBalance = ?, Notes = ? WHERE AcctID = ?"
        params =  (self.Type, self.Name, self.Bank, self.AccountNo, self.Currency, self.StartingBalance, self.Notes, self.AcctID)        
        #logging.logSQL (sql)
        result = db.execute(sql,params)
        return result == 1

    @classmethod
    def deleteAccount(cls, db, AcctID):
        logging.logDebug("Delete Account:" + AcctID)
        sql = "DELETE FROM tbl_account where AcctID = ?"  
        params = (AcctID)
        #logging.logSQL (sql)
        result = db.execute(sql,params)
        return result == 1

    # View from database
    @classmethod
    def viewAccount(cls, db, AcctID):
        logging.logDebug("View Account:" + AcctID)
        sql = "SELECT * FROM tbl_account where AcctID = ?" 
        params = (AcctID) 
        #logging.logSQL (sql)
        data = db.query(sql,params)
        if data is not None:
            a = Account(AcctID,data[1],data[2],data[3],data[4],data[5],data[6],data[7])
            return a
        else:
            return None

    @classmethod
    def listAccount(cls, db, params):
        logging.logDebug("List Account")
        sql = "SELECT * FROM tbl_account" 
        #params = (AcctID) 
        #logging.logSQL (sql)
        data = db.list(sql,())
        if data is not None:
            results = []
            for row in data:
                a = Account(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                results.append(a)
            return results
        else:
            return None

    def toString(self):
        return "Type %s %s %s[%s] Balance %s %d" % (self.Type,self.Name, self.Bank, self.AccountNo, self.Currency, self.StartingBalance)
        # return "Account Type: " + str(self.Type) + ":" + self.Name + " " + self.Bank + "[" + self.AccountNo + "]" + self.Currency + str(self.StartingBalance)


class AccountController:
    def process(self,argv,db):
        if argv[0] == 'ac':
            return self.createAccount(argv,db)
        if argv[0] == 'av':
            return self.view(argv,db)
        if argv[0] == 'au':
            return self.update(argv,db)
        if argv[0] == 'ad':
            return self.delete(argv,db)
        if argv[0] == 'al':
            return self.list(argv,db)

    def update(self,argv,db):
        logging.logDebug ("Update " + argv[1])
        try:
            if len(argv) == 9:
                a = Account(argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7],argv[8])
                success = a.update(db)
                if success: 
                    logging.output("Update Account successful")
                else:
                    logging.output("Update Account not successful")

        except Exception as e:
            logging.logException (e)
            return False
        return True

    def delete(self,argv,db):
        logging.logDebug ("Delete " + argv[1])
        try:
            if len(argv) >= 2:
                success = Account.deleteAccount(db,argv[1])
                if success: 
                    logging.output("Delete Account successful")
                else:
                    logging.output("Delete Account not successful")
        except Exception as e:
            logging.logException (e)
            return False
        return True

    def list(self,argv,db):
        logging.logDebug ("List " + argv[1])
        try:
            if len(argv) >= 2:
                list = Account.listAccount(db,argv)
                # todo Print the list
                logging.output("Print the list")
                for a in list:
                    print (a.toString())
        except Exception as e:
            logging.logException (e)
            return False
        return True


    def view(self,argv,db):
        logging.logDebug ("View " + argv[1])
        try:
            if len(argv) >= 2:
                a = Account.viewAccount(db,argv[1])
                if a is None:
                    logging.output ("No data found")
                else:
                    logging.output(a.toString());
        except Exception as e:
            logging.logException (e)
            return False
        return True

    def createAccount(self,argv,db):
        try:
            if len(argv) == 7:
                a = Account('AcctID',argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],'')

            if len(argv) == 8:
                a = Account('AcctID',argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7])
            a.create(db)     
        except Exception as e:
            logging.logException (e)
        except UnboundLocalError as valerr:
            print ("ac [Type: 1|2] [Name] [Bank] [AccountNo] [Currency MYR|USD] [Starting Balance] [Notes]")
        except:
            # print help
            print ("ac [Type: 1|2] [Name] [Bank] [AccountNo] [Currency MYR|USD] [Starting Balance] [Notes]")

        return True;