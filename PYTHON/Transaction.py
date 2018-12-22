import Logging as logging
class Transaction:

    def __init__(self, TransactionID, SubID, Type, Level1, Level2, AcctID, Currency, Amount, TransactionDate, Payee, Notes):
        self.TransactionID = TransactionID
        self.SubID = SubID
        self.Type = Type
        self.Level1 = Level1
        self.Level2 = Level2
        self.AcctID = AcctID
        self.Currency = Currency
        self.Amount = Amount
        self.TransactionDate = TransactionDate
        self.Payee = Payee
        self.Notes = Notes

    # Save in database

    def create(self,db):
        sql = "INSERT INTO tbl_transaction (SubID,Type,Level1,Level2,AcctID,Currency, Amount , TransactionDate , Payee , Notes ) VALUES (?,?,?,?,?,?,?,?,?,?)" 
        params = (self.SubID, self.Type, self.Level1, self.Level2, self.AcctID, self.Currency, self.Amount, self.TransactionDate , self.Payee , self.Notes )
        id = db.insertpk(sql,params)
        return id

    def update(self,db):
        sql = "UPDATE tbl_transaction SET SubID = ?, Type = ?, Level1 = ?, Level2 = ?, AcctID = ?, Currency =?, Amount = ? ,TransactionDate = ?, Payee =? , Notes = ? \
            WHERE TransactionID = ?" 
        params = (self.SubID, self.Type, self.Level1, self.Level2, self.AcctID, self.Currency, self.Amount, self.TransactionDate , self.Payee , self.Notes, self.TransactionID )
        result = db.execute(sql,params)
        return result == 1

    def delete(self, db):
        logging.logDebug("Delete Transaction: " + self.toString())
        sql = "DELETE FROM tbl_transaction where TransactionID = ?"  
        params = [self.TransactionID]
        result = db.execute(sql,params)
        return result >= 1

    def tag(self, db, id):
        logging.logDebug("Tag Transaction: " + self.TransactionID + " " + id)
        sql = "INSERT INTO tbl_transaction_tag VALUES (?,?)"  
        params = [self.TransactionID , id]
        result = db.execute(sql,params)
        return result >= 1

    def untag(self, db, id):
        logging.logDebug("Untag Transaction: " + self.TransactionID + " " +  id)
        sql = "DELETE FROM tbl_transaction_tag WHERE TransactionID = ? AND TagID = ?"  
        params = [self.TransactionID , id]
        result = db.execute(sql,params)
        return result >= 1

    def view(self, db):
        logging.logDebug("View Transaction: " + self.TransactionID)
        sql = "SELECT * FROM tbl_transaction where TransactionID = ?"  
        params = [self.TransactionID]
        data = db.query(sql,params)
        if data is not None:
            t = Transaction(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10])
            return t
        else:
            return None

    @classmethod
    def list(cls, db, params):
        logging.logDebug("List Transactions")
        sql = "SELECT * FROM tbl_transaction" 
        data = db.list(sql,())
        if data is not None:
            results = []
            for row in data:
                t = Transaction(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
                results.append(t)
            return results
        else:
            return None

    def toString(self):
        return "Transaction %s %s %s %s %s%s" % (self.TransactionID,self.Type, self.Level1, self.Level2, self.Currency, self.Amount)

class TransactionController:
    def process(self,argv,db):
        if argv[0] == 'tc':
            return self.create(argv,db)
        if argv[0] == 'td':
            return self.delete(argv,db)
        if argv[0] == 'tv':
            return self.view(argv,db)
        if argv[0] == 'tl':
            return self.list(argv,db)
        if argv[0] == 'tu':
            return self.update(argv,db)
        if argv[0] == 'tt':
            return self.tag(argv,db)

    def view(self,argv,db):
        logging.logDebug ("View")
        try:
            if len(argv) >= 2:
                # Create the object
                t = Transaction(argv[1],'','','','','','','','','','')
                t = t.view(db)
                if t is not None: 
                    logging.output(t.toString())
                else:
                    logging.output("Transaction not found")
            else:
                raise ValueError('Incorrect number of parameters')                
        except ValueError as e:
            logging.output(str(e));
            logging.output ("td [TransactionID]")
        except Exception as e:
            logging.logException (e)
            return False
        return True

    def tag(self,argv,db):
        logging.logDebug ("Tag")
        try:
            if len(argv) >= 3:
                # Create the object
                t = Transaction(argv[1],'','','','','','','','','','')
                for x in argv[2:]:
                    # Untag first so no errors when inserting duplicates
                    success = t.untag(db,x)
                    success = t.tag(db,x)
            else:
                raise ValueError('Incorrect number of parameters')                
        except ValueError as e:
            logging.output(str(e));
            logging.output ("tt [TransactionID] [TagID]*")
        except Exception as e:
            logging.logException (e)
            return False
        return True


    def delete(self,argv,db):
        logging.logDebug ("Delete")
        try:
            if len(argv) >= 2:
                # Create the object
                t = Transaction(argv[1],'','','','','','','','','','')
                success = t.delete(db)
                if success: 
                    logging.output("Delete Transaction successful")
                else:
                    logging.output("Delete Transaction not successful")
            else:
                raise ValueError('Incorrect number of parameters')                
        except ValueError as e:
            logging.output(str(e));
            logging.output ("td [TransactionID]")
        except Exception as e:
            logging.logException (e)
            return False
        return True

    def list(self,argv,db):
        logging.logDebug ("List")
        try:
            if len(argv) >= 2:
                list = Transaction.list(db,argv)
                # todo Print the list
                logging.output("Print the list")
                for t in list:
                    logging.output (t.toString())
        except Exception as e:
            logging.logException (e)
            return False
        return True

    def update(self,argv,db):
        try:
            if len(argv) == 12:
                # Create the object
                t = Transaction(argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7],argv[8],argv[9],argv[10], argv[11])
                success = t.update(db)
                if success: 
                    logging.output("Update Transaction successful")
                else:
                    logging.output("Update Transaction not successful")
            else:
                raise ValueError('Incorrect number of parameters')
        except ValueError as e:
            logging.output(str(e));
            logging.output ("tu [TransactionID] [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        except Exception as e:
            logging.logException (e)
            logging.output ("tu [TransactionID] [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        except:
            # print help
            logging.output ("tu [TransactionID] [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        return True;

    def create(self,argv,db):
        try:
            if len(argv) == 11:
                # Create the object
                t = Transaction("TRANSID",argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7],argv[8],argv[9],argv[10])
                id = t.create(db)
                if id != 0: 
                    logging.output("Create Transaction successful")
                else:
                    logging.output("Create Transaction not successful")
            else:
                raise ValueError('Incorrect number of parameters')
        except ValueError as e:
            logging.output(str(e));
            logging.output ("tc [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        except Exception as e:
            logging.logException (e)
            logging.output ("tc [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        except:
            # print help
            logging.output ("tc [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        return True;