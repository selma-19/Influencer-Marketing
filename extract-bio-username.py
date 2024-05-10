import os
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.InfluencersMarketing
collection = db.NewInfluencers

# Directory containing the files
directory = "C:\\Users\\chadha\\Desktop\\users_influencers"

for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                fields = line.strip().split('\t')
                if len(fields) >= 7:  # Ensure the line has enough fields
                    name = fields[0]
                    category = fields[6]
                    bio = fields[7] if len(fields) > 7 else ''

                    if not name and not category and not bio :
                        continue
                    else:
                        # Create JSON object
                        json_obj = {
                            "Name": name,
                            "Category": category,
                            "Bio": bio
                        }
                        print(json_obj)

                        # Insert JSON object into MongoDB collection
                        collection.insert_one(json_obj)
            except Exception as e:
                print(f"An exception occurred: {e}. Skipping this user")
