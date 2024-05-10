from pymongo import MongoClient
client = MongoClient("localhost", 27017)
db = client.InfluencersMarketing
collection = db.NewInfluencers
posts = db.posts #modify this to your mongo post collection's name