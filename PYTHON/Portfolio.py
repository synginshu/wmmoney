import Logging as logging
from Transaction import Transaction

class Portfolio(Transaction):

    def __init__(self, TransactionID, SubID, Type, Level1, Level2, AcctID, Currency, Amount, TransactionDate, Payee, Notes, SecurityCode, Units, PricePerUnit, Fees):
        Transaction.__init__(self,TransactionID,SubID,Type, Level1, Level2, AcctID, Currency, Amount, TransactionDate, Payee, Notes)
        self.SecurityCode = SecurityCode
        self.Units = Units
        self.PricePerUnit = PricePerUnit
        self.Fees = Fees

    # Save in database
    def create(self,db):
        self.TransactionID = Transaction.create(self,db)
        sql = "INSERT INTO tbl_transaction_portfolio (TransactionID, SecurityCode, Units, PricePerUnit, Fees) VALUES (?,?,?,?,?)" 
        params = (self.TransactionID, self.SecurityCode, self.Units, self.PricePerUnit, self.Fees )
        logging.logDebug(params)
        result = db.execute(sql,params)
        return result == 1

    def update(self,db):
        Transaction.update(self,db)
        sql = "UPDATE tbl_transaction_portfolio SET SecurityCode = ?, Units = ?, PricePerUnit = ?, Fees = ? \
            WHERE TransactionID = ?" 
        params = (self.SecurityCode, self.Units, self.PricePerUnit, self.Fees,  self.TransactionID )
        result = db.execute(sql,params)
        return result == 1

    def delete(self, db):
        logging.logDebug("Delete Portfolio: " + self.toString())
        Transaction.delete(self,db)
        sql = "DELETE FROM tbl_transaction_portfolio where TransactionID = ?"  
        params = [self.TransactionID]
        result = db.execute(sql,params)
        return result >= 1

    def view(self, db):
        logging.logDebug("View Portfolio: " + self.TransactionID)
        sql = "SELECT * FROM tbl_transaction inner join  tbl_transaction_portfolio on tbl_transaction.TransactionID = tbl_transaction_portfolio.TransactionID \
        where tbl_transaction.TransactionID = ?"  
        params = [self.TransactionID]
        data = db.query(sql,params)
        if data is not None:
            #Skip data 11 because its the transaction id again
            t = Portfolio(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[12],data[13],data[14],data[15])
            return t
        else:
            return None

    @classmethod
    def list(cls, db, params):
        logging.logDebug("List Transactions")
        sql = "SELECT T.* ,P.* FROM tbl_transaction_portfolio as P inner join tbl_transaction as T on T.TransactionID = P.TransactionID" 
        rows = db.list(sql,())
        if rows is not None:
            results = []
            for data in rows:
                t = Portfolio(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[12],data[13],data[14],data[15])
                results.append(t)
            return results
        else:
            return None

    def toString(self):
        return "Portfolio %s %s %s %s %s%s %s %s" % (self.TransactionID,self.Type, self.Level1, self.Level2, self.Currency, self.Amount, self.SecurityCode, self.PricePerUnit)

class PortfolioController:
    def process(self,argv,db):
        if argv[0] == 'pc':
            return self.create(argv,db)
        if argv[0] == 'pd':
            return self.delete(argv,db)
        if argv[0] == 'pv':
            return self.view(argv,db)
        if argv[0] == 'pl':
            return self.list(argv,db)
        if argv[0] == 'pu':
            return self.update(argv,db)

    def view(self,argv,db):
        logging.logDebug ("View")
        try:
            if len(argv) >= 2:
                # Create the object
                t = Portfolio(argv[1],'','','','','','','','','','','','','','')
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

    def delete(self,argv,db):
        logging.logDebug ("Delete")
        try:
            if len(argv) >= 2:
                # Create the object
                t = Portfolio(argv[1],'','','','','','','','','','','','','','')
                success = t.delete(db)
                if success: 
                    logging.output("Delete Portfolio successful")
                else:
                    logging.output("Delete Portfolio not successful")
            else:
                raise ValueError('Incorrect number of parameters')                
        except ValueError as e:
            logging.output(str(e));
            logging.output ("pd [TransactionID]")
        except Exception as e:
            logging.logException (e)
            return False
        return True

    def list(self,argv,db):
        logging.logDebug ("List")
        try:
            if len(argv) >= 2:
                list = Portfolio.list(db,argv)
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
            if len(argv) == 16:
                # Create the object
                t = Portfolio(argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7],argv[8],argv[9],argv[10], argv[11],argv[12],argv[13],argv[14],argv[15])
                success = t.update(db)
                if success: 
                    logging.output("Update Portfolio successful")
                else:
                    logging.output("Update Portfolio not successful")
            else:
                raise ValueError('Incorrect number of parameters')
        except ValueError as e:
            logging.output(str(e));
            logging.output ("pu [TransactionID] [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes] [SecurityCode] [Units] [PricePerUnit] [Fees]")
        except Exception as e:
            logging.logException (e)
            logging.output ("pu [TransactionID] [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        except:
            # print help
            logging.output ("pu [TransactionID] [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        return True;

    def create(self,argv,db):
        try:
            if len(argv) == 15:
                # Create the object
                t = Portfolio("TRANSID",argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7],argv[8],argv[9],argv[10], argv[11],argv[12],argv[13],argv[14])
                success = t.create(db)
                if success: 
                    logging.output("Create Portfolio successful")
                else:
                    logging.output("Create Portfolio not successful")
            else:
                raise ValueError('Incorrect number of parameters')
        except ValueError as e:
            logging.output(str(e));
            logging.output ("pc [TransactionID] [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        except Exception as e:
            logging.logException (e)
            logging.output ("pc [TransactionID] [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        except:
            # print help
            logging.output ("pc [TransactionID] [SubID] [Type] [Level1] [Level2] [AcctID] [Currency] [Amount] [TransactionDate] [Payee] [Notes]")
        return True;