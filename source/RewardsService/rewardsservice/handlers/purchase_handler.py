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

        self.write('email: %s total: %s' % (email, total))


        #db.purchases.insert({})

    @coroutine
    def get(self):
        email = self.get_query_argument('email')
        total = self.get_query_argument('total')



        self.write('email: %s total: %s' % (email, total))



    def updateUser(self, email, total):
        #process input
        if type(total) == str:
            total = float(total)
        total = int(total)

        #setup db connection
        self.client = MongoClient("mongodb", 27017)
        self.db = client["Rewards"]

        user =  self.db.customer.find_one({'email': email})
        if user != None:
            user['points'] += total

        user = self.calculateStats(user)

        self.db.customer.update({'email': user['email']}, user, {upsert: True})



    def getNextTier(self, user):
        nextTier =  self.db.rewards.find_one({'points': {'$gt': user['points']}})
        if nextTier == None:
            nextTier = {
                'tier' : None,               
                'rewardName' : None,       
                'points' : None
            }
        return nextTier

    def getCurrentTier(self, user):
        currentTier =  self.db.rewards.find_one({'points': {'$lt': user['points']}})
        if currentTier == None:
            currentTier = {
                'tier' : None,
                'rewardName' : None,
                'points' : 0
            }
        return currentTier

    def calculateStats(self, user):

        nextTier =  self.getNextTier(user)
        currentTier =  self.getCurrentTier(user)

        user['nextTier']         = nextTier['tier']                   
        user['nextTierName']     = nextTier['rewardName']             


        user['tier']       = currentTier['tier']      
        user['rewardName'] = currentTier['rewardName']

        user['nextTierProgress']   = (nextTier['points'] - user['points'])/(nextTier['points']-currentTier['points']) 

        return user

