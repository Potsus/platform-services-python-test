import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class PurchaseHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
