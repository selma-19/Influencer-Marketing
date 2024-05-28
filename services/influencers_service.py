import configparser
import logging

from shared.mongo import MongoConnection


class InfluencersService:
    def __init__(self, mongo_connection: MongoConnection):
        db = mongo_connection.get_database()
        config = configparser.ConfigParser()
        config.read('../config.ini')
        mongo_config = config['MongoDB']  # Access the MongoDB section

        self.posts_collection = db[mongo_config.get("POSTS_COLLECTION", "posts")]
        self.influencers_collection = db[mongo_config.get("INFLUENCERS_COLLECTION", "Influencers")]
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_influencers(self):
        try:
            influencers = list(self.influencers_collection.find())
            logging.info("Fetched %d influencers", len(influencers))
            return influencers
        except Exception as e:
            logging.error("An error occurred while fetching influencers: %s", str(e))
            return []

    def get_posts(self):
        try:
            posts = list(self.posts_collection.find())
            logging.info("Fetched %d posts", len(posts))
            return posts
        except Exception as e:
            logging.error("An error occurred while fetching posts: %s", str(e))
            return []

    def update_influencer(self, influencer, key, value):
        try:
            filter = {'_id': influencer['_id']}
            update = {'$set': {key: value}}
            result = self.influencers_collection.update_one(filter, update)
            if result.modified_count > 0:
                logging.info("Updated influencer %s with %s: %s", influencer['_id'], key, value)
            else:
                logging.warning("No influencer found with id %s to update", influencer['_id'])
            return result
        except Exception as e:
            logging.error("An error occurred while updating an influencer: %s", str(e))
            return None

    def update_post(self, post, key, value):
        try:
            filter = {'_id': post['_id']}
            update = {'$set': {key: value}}
            result = self.posts_collection.update_one(filter, update)
            if result.modified_count > 0:
                logging.info("Updated post %s with %s: %s", post['_id'], key, value)
            else:
                logging.warning("No post found with id %s to update", post['_id'])
            return result
        except Exception as e:
            logging.error("An error occurred while updating a post: %s", str(e))
            return None
