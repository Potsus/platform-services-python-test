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

        user = list(self.updateUser(email, total))
        #self.write(json.dumps(user))

    @coroutine
    def get(self):
        email = self.get_query_argument('email')
        total = self.get_query_argument('total')

        user = self.updateUser(email, total)
        #self.write(json.dumps(user))



    def updateUser(self, email, total):
        #process input
        if type(total) == str:
            total = float(total)
        total = int(total)

        #setup db connection
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]

        user = self.getUser(email)
        user['points'] += total

        user = self.calculateStats(user)

        self.db.customer.update({'email': user['email']}, user, True)
        return user


    def getUser(self, email):
        user =  self.db.customer.find_one({'email': email})
        if user == None:
            user = {
                'email' : email,
                'points' : 0
            }
        return user


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
        currentTier =  list(self.db.rewards.find({'points': {'$lt': user['points']}}).sort('points', -1))
        currentTier = currentTier[0] if len(currentTier) > 0 else None
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

        user['tier']       = currentTier['tier']      
        user['rewardName'] = currentTier['rewardName']

        user['nextTier']         = nextTier['tier']                   
        user['nextTierName']     = nextTier['rewardName']  

        progress = float(nextTier['points'] - user['points'])/(nextTier['points']-currentTier['points'])
        user['nextTierProgress']   =  round((1-progress), 2)

        return user

