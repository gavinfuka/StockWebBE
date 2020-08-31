import couchdb 

#https://gist.github.com/marians/8e41fc817f04de7c4a70

class CouchDB:
    def __init__(self, HTTP, USERNAME, PASSWORD, URL):
        db_url = HTTP + "://" + USERNAME + ":"+ PASSWORD +"@" + URL
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

    def Update(self,dbName,doc):
        self.Connect(dbName).update(doc)

    def Insert(self,dbName,doc, _id=None):
        self.Connect(dbName).save(doc)

    def getDocQ(self,dbName,_id):
        return self.Connect(dbName)[_id]
        