import pymongo

class CompanyprofilescrawlPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['Company_profiles']
        self.collection = db['idx_profiles']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
