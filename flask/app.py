from bertopic import BERTopic
from flask import Flask, request, jsonify

from cleaning import clean_and_process_content
from dataParser import parse_user
# TODO: Make it work with this
# from dataScraper.scraper import scrape_user
from scraper import scrape_user

# Load the BERTopic model
model_path = "model-training/model/bert_9"
topic_model = BERTopic.load(model_path)
topic_labels = topic_model.generate_topic_labels()
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data['text']

    # Get topic predictions
    topics, probs = topic_model.transform([text])

    return jsonify(
        {'topics': topics.tolist(), 'probs': probs.tolist()})  # return jsonify({'topics': topic_labels.tolist()})


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    name = data['name']
    user_data = (parse_user(scrape_user(name)['data']['user']))
    bio = user_data['bio']
    category = user_data['category']
    return jsonify({'bio': bio, 'category': category})


@app.route('/predict_user', methods=['POST'])
def full_process():
    data = request.json
    name = data['name']

    # Step 1: Scrape the user data
    scraped_data = scrape_user(name)
    user_data = parse_user(scraped_data['data']['user'])

    # Step 2: Predict the category based on user data
    bio = user_data['bio']
    category = user_data['category']
    if (category is not None):
        bio += category
    cleaned_bio = clean_and_process_content(bio)
    topics, probs = topic_model.transform([cleaned_bio])

    return jsonify(
        {'bio': cleaned_bio, 'topics': topics.tolist(), 'probs': probs.tolist()})  # return jsonify({'topics': topic_labels})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
