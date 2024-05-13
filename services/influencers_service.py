import configparser

from shared.mongo import MongoConnection


class InfluencersService:
    def __init__(self, mongo_connection: MongoConnection):
        db = mongo_connection.get_database()
        config = configparser.ConfigParser()
        config.read('../config.ini')
        mongo_config = config['MongoDB']  # Access the MongoDB section

        self.posts_collection = db[mongo_config.get("POSTS_COLLECTION", "Posts")]
        self.influencers_collection = db[mongo_config.get("INFLUENCERS_COLLECTION", "Influencers")]

    def get_influencers(self):
        try:
            return list(self.influencers_collection.find())
        except Exception as e:
            print(f"An error occurred while fetching influencers: {e}")
            return []

    def get_posts(self):
        try:
            return list(self.posts_collection.find())
        except Exception as e:
            print(f"An error occurred while fetching posts: {e}")
            return []

    def update_influencer(self, influencer, key, value):
        try:
            filter = {'_id': influencer['_id']}
            update = {'$set': {key: value}}
            return self.influencers_collection.update_one(filter, update)
        except Exception as e:
            print(f"An error occurred while updating an influencer: {e}")
            return None

    def update_post(self, post, key, value):
        try:
            filter = {'_id': post['_id']}
            update = {'$set': {key: value}}
            return self.posts_collection.update_one(filter, update)
        except Exception as e:
            print(f"An error occurred while updating a post: {e}")
            return None
