import Logging as logging
class Tag:

    def __init__(self, TagID, Description):
        self.TagID = TagID
        self.Description = Description

    # Save in database
    def create(self,db):
        sql = "INSERT INTO tbl_tag (Description) VALUES (?)" 
        params = [self.Description]
        result = db.execute(sql,params)
        return result == 1

    def delete(self, db):
        logging.logDebug("Delete Tag: " + self.toString())
        sql = "DELETE FROM tbl_tag where Description = ?"  
        params = [self.Description]
        result = db.execute(sql,params)
        return result >= 1

    @classmethod
    def list(cls, db, params):
        logging.logDebug("List Tags")
        sql = "SELECT * FROM tbl_tag" 
        data = db.list(sql,())
        if data is not None:
            results = []
            for row in data:
                t = Tag(row[0],row[1])
                results.append(t)
            return results
        else:
            return None

    def toString(self):
        return "Tag %s %s" % (self.TagID,self.Description)

class TagController:
    def process(self,argv,db):
        if argv[0] == 'gc':
            return self.create(argv,db)
        if argv[0] == 'gd':
            return self.delete(argv,db)
        if argv[0] == 'gl':
            return self.list(argv,db)

    def delete(self,argv,db):
        logging.logDebug ("Delete")
        try:
            if len(argv) >= 2:
                # Create the object
                tag = Tag('',argv[1])
                success = tag.delete(db)
                if success: 
                    logging.output("Delete Tag successful")
                else:
                    logging.output("Delete Tag not successful")
        except Exception as e:
            logging.logException (e)
            return False
        return True

    def list(self,argv,db):
        logging.logDebug ("List")
        try:
            if len(argv) >= 2:
                list = Tag.list(db,argv)
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
            if len(argv) >= 2:
                # Create the object
                tag = Tag("TAGID",argv[1])
                success = tag.create(db)
                if success: 
                    logging.output("Create Tag successful")
                else:
                    logging.output("Create Tag not successful")
        except Exception as e:
            logging.logException (e)
        except:
            # print help
            print ("gc [Description]")
        return True;