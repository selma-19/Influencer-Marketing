from flask import Flask, request, jsonify
import gensim
import pyLDAvis.gensim
import pickle

# Load the LDA model and other necessary objects
lda_model = gensim.models.ldamodel.LdaModel.load('lda_model.pkl')
id2word = gensim.corpora.Dictionary.load('id2word.pkl')
corpus = pickle.load(open('corpus.pkl', 'rb'))

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Process the input text
    text = data['text']
    tokens = gensim.utils.simple_preprocess(text, deacc=True)
    bow = id2word.doc2bow(tokens)
    topics = lda_model.get_document_topics(bow)
    return jsonify(topics)

@app.route('/visualize', methods=['GET'])
def visualize():
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word, mds="mmds", R=30, lambda_step=0.01)
    return pyLDAvis.display(vis).data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
