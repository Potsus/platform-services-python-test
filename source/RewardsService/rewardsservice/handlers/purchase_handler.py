import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class PurchaseHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        #process the input
        email = self.get_body_argument('email')
        total = self.get_body_argument('total')
        if type(total) == str:
            total = float(total)
        total = int(total)

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        user =  db.customer.find_one({'email': email})
        if user == None:
            pass
        else:
            pass

        self.write('email: %s total: %s' % (email, total))


        #db.purchases.insert({})

    @coroutine
    def get(self):
        email = self.get_query_argument('email')
        total = self.get_query_argument('total')

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]




        self.write('email: %s total: %s' % (email, total))