from bson.json_util import dumps
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class ClienteleHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        clientele = list(db.customer.find({}, {"_id": 0}))
        self.write(dumps(clientele))
