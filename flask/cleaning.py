import logging
import re
import string

import nltk
import spacy
from deep_translator import GoogleTranslator
from nltk.corpus import stopwords

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from unidecode import unidecode

nltk.download('stopwords')
stopwords_en = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
translator = GoogleTranslator(source='auto', target='en')


def clean_and_process_content(content):
    """
    This performs URL removal, special character cleaning, emoji removal, translation, stopword removal, and lemmatization.
     Args:
        posts (list): List of posts to process.
        key (str): The key in the post dictionary that contains the content to be cleaned.

    Returns:
        None
    """

    try:
        # Removing URLs
        content = re.sub(r'http\S+', '', content)

        # Removing Special Characters
        content = re.sub(r'\W+', ' ', content)

        # Removing Emojis
        content = unidecode(content)

        # Translating text (if not in English)
        content = translator.translate(content)
    except Exception as e:
        logging.error(f"An exception occurred during cleaning or translation: {e}. Skipping this caption.")

    content = content.lower().translate(str.maketrans('', '', string.punctuation))

    # Removing Stopwords
    words = content.split()
    content = ' '.join([word for word in words if word not in stopwords_en])

    # Lemmatizing Text
    try:
        doc = nlp(content)
        lemmatized_content = " ".join([token.lemma_ for token in doc])
    except Exception as e:
        logging.error(f"Lemmatization error: {e}.")

    return content
