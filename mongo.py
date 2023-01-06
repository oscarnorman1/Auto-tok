import config
import pymongo


class Mongo:

    def __init__(self):
        self.mongo_client = pymongo.MongoClient(config.getProperty("dburl"))
        self.db = self.mongo_client['RedditPosts']
        self.collection = self.db['posts']

    def save(self, dict):
        self.collection.insert_one(dict)

    def check_if_exists(self, post):
        for x in self.collection.find():
            if x['title'] == post['title']:
                return True
            if x['content'] == post['content']:
                return True
        return False
