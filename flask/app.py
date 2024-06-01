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


def get_topic_details(topic_id):
    return {'id': topic_id, 'label': topic_labels[topic_id+1]}


def scrape_user_data(name):
    scraped_data = scrape_user(name)
    if 'data' not in scraped_data or 'user' not in scraped_data['data']:
        raise ValueError("Invalid user data received")

    user_data = parse_user(scraped_data['data']['user'])
    bio = user_data['bio']
    category = user_data['category']
    result = {'bio': bio, 'category': category}
    return result


def predict_topics(text):
    topics, probs = topic_model.transform([text])
    topic_details = get_topic_details(topics[0])
    return topic_details, probs.tolist()


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if 'text' not in data:
            return jsonify({'error': 'Missing text input'}), 400

        text = data['text']

        # Get topic predictions
        topic_details, probs = predict_topics(text)
        topic_label = topic_details['label']
        return jsonify({'label': topic_label, 'probs': probs})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        if 'name' not in data:
            return jsonify({'error': 'Missing username input'}), 400

        name = data['name']

        # Scrape user data

        result = scrape_user_data(name)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/predict_user', methods=['POST'])
def full_process():
    try:
        data = request.json
        if 'name' not in data:
            return jsonify({'error': 'Missing username input'}), 400

        name = data['name']
        user_data = scrape_user_data(name)
        bio = user_data['bio']
        category = user_data['category']
        if category is not None:
            bio += ' ' + category

        cleaned_bio = clean_and_process_content(bio)
        topic_details, probs = predict_topics(cleaned_bio)

        result = {'bio': cleaned_bio, 'topics': topic_details, 'probs': probs}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
