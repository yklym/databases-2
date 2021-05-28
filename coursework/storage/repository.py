from pymongo import MongoClient


class LotRepository:
    def __init__(self):
        client = MongoClient('localhost', 43000)
        db = client['LotsDB']

        self.db = db
        self.client = client
        self.lots_collection = db['lots']

    def insert(self, lot):
        try:
            self.lots_collection.insert_one(lot)
            return True
        except:
            self.lots_collection.update_one({'_id': lot['_id']}, {'$set': lot})
            return False

    def find_document(self, elements):
        results = self.lots_collection.find(elements)
        return [r for r in results]

lot_repository = LotRepository()