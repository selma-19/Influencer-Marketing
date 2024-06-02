from bertopic import BERTopic
import pickle

# Load the BERTopic model
model_path = "./model-training/model/bert_9"
topic_model = BERTopic.load(model_path)

output_file = f'flask/bert_9.pkl'

# Save the model using pickle
with open(output_file, 'wb') as f_out:
    pickle.dump(topic_model, f_out)