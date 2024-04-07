import shared.mongo as mongo
def get_influencers():
	return mongo.collection.find()
def update_influencer(influencer,key,value):
	filter = {'_id': influencer['_id']}
	update = {'$set': {key: value}}
	return mongo.collection.update_one(filter, update)
