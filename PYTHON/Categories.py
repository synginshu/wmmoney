import Logging as logging
class Category:

    def __init__(self, Type, Level1, Level2):
        self.Type = Type
        self.Level1 = Level1
        self.Level2 = Level2

    # Save in database
    def create(self,db):
        sql = "INSERT INTO tbl_categories (Type,Level1,Level2) VALUES (?,?,?)" 
        params = (self.Type, self.Level1, self.Level2)
        # logging.logSQL (sql,params)
        result = db.execute(sql,params)
        return result == 1

    def delete(self, db):
        logging.logDebug("Delete Category: " + self.toString())
        sql = "DELETE FROM tbl_categories where Type = ? AND Level1 = ? AND Level2 = ?"  
        params = (self.Type, self.Level1, self.Level2)
        result = db.execute(sql,params)
        return result == 1

    @classmethod
    def list(cls, db, params):
        logging.logDebug("List Categories")
        sql = "SELECT * FROM tbl_categories" 
        data = db.list(sql,())
        if data is not None:
            results = []
            for row in data:
                c = Category(row[0],row[1],row[2])
                results.append(c)
            return results
        else:
            return None

    def toString(self):
        return "Category %s %s %s" % (self.Type,self.Level1, self.Level2)

class CategoryController:
    def process(self,argv,db):
        if argv[0] == 'cc':
            return self.create(argv,db)
        if argv[0] == 'cd':
            return self.delete(argv,db)
        if argv[0] == 'cl':
            return self.list(argv,db)

    def delete(self,argv,db):
        logging.logDebug ("Delete")
        try:
            if len(argv) >= 4:
                # Create the object
                cat = Category(argv[1],argv[2],argv[3])
                success = cat.delete(db)
                if success: 
                    logging.output("Delete Category successful")
                else:
                    logging.output("Delete Category not successful")
        except Exception as e:
            logging.logException (e)
            return False
        return True

    def list(self,argv,db):
        logging.logDebug ("List")
        try:
            if len(argv) >= 2:
                list = Category.list(db,argv)
                # todo Print the list
                logging.output("Print the list")
                for a in list:
                    print (a.toString())
        except Exception as e:
            logging.logException (e)
            return False
        return True

    def create(self,argv,db):
        try:
            if len(argv) >= 4:
                # Create the object
                cat = Category(argv[1],argv[2],argv[3])
                success = cat.create(db)
                if success: 
                    logging.output("Create Category successful")
                else:
                    logging.output("Create Category not successful")
        except Exception as e:
            logging.logException (e)
        except:
            # print help
            print ("cc [Type: 1|2] [Level1] [Level2]")
        return True;