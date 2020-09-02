import couchdb 

#https://gist.github.com/marians/8e41fc817f04de7c4a70

class CouchDB:
    def __init__(self, config):
        db_url = config["HTTP"] + "://" + config["USERNAME"] + ":"+ config["PASSWORD"] +"@" + config["URL"]
        self.couchserver = couchdb.Server(db_url)

    
    def Connect(self,dbName):
        if dbName in self.couchserver:
           return self.couchserver[dbName]
        else:
            print('[x]Database:%s does not exist'%(dbName))


    def Find(self,dbName, skip=0, limit=100, fields = [], sort = [], selector = {}):
        query={}
        query['selector']= selector
        query['limit'] = limit
        return_map = self.Connect(dbName).find(query)
        return return_map


    def List(self,dbName):
        return_map = self.Connect(dbName).list()
        return return_map


    def Insert(self,dbName,doc, _id=None):
        try:
            if _id:
                doc["_id"] = _id
            self.Connect(dbName).save(doc)
        except:
            print("[x] CouchDB :: %s :: Insert Doc Failed"%_id)


    def getDocQ(self,dbName,_id):
        return self.Connect(dbName)[_id]


    def Update(self,dbName,doc, _id):
        try:
            OldDoc = self.Connect(dbName).get(_id)
            if not OldDoc:
                return self.Insert(dbName,doc, _id)

            _rev = OldDoc['_rev']
            del OldDoc['_rev']
            if not OldDoc == doc:
                doc["_rev"] = _rev
                self.Insert(dbName,doc, _id)
            else:
                print("[x] CouchDB :: %s No need to update"%_id)
        except:
            print("[x] CouchDB :: %s :: Update Doc Failed"%_id)
        