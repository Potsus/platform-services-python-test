import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class PurchaseHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        email = self.get_body_argument('email')
        total = self.get_body_argument('total')
        self.write('email: %s total: %s' % (email, total))


        #db.purchases.insert({})

    @coroutine
    def get(self):
        email = self.get_query_argument('email')
        total = self.get_query_argument('total')
        self.write('email: %s total: %s' % (email, total))