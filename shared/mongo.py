from pymongo import MongoClient
client = MongoClient("localhost", 27017)
db = client.InfluencersMarketing
collection = db.Influencers
posts = db.posts_8 #modify this to your mongo post collection's name