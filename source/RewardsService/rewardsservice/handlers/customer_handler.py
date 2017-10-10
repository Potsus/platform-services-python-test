from bson.json_util import dumps
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        email = self.get_query_argument('email')

        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]

        user =  self.db.customer.find_one({'email': email})
        self.write(dumps(user))
