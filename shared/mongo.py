from pymongo import MongoClient
import re
client = MongoClient("localhost", 27017)
db = client.InfluencersMarketing
collection = db.NewInfluencers
posts = db.Posts #modify this to your mongo post collection's name

