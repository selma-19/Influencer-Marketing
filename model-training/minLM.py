
from transformers import AutoTokenizer, AutoModelForSequenceClassification,TrainingArguments, Trainer
from datasets import Dataset


#%%

data = {
    "text": [
        "workout work out fit healthy gains muscle strength cardio gym ",# Fitness
        "cook delicious recipe ingredient  dessert cake ",  # Food
        "skincare routine makeup style beauty outfit model routine products ",  # Beauty
    ],
    "label": [
        0,  # Fitness
        1,  # Food
        2,  # Beauty

    ]
}

dataset = Dataset.from_dict(data)
train_test_split = dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split['train']
eval_dataset = train_test_split['test']
#%%
model_name = "microsoft/MiniLM-L12-H384-uncased"
number_of_categories=3
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=number_of_categories)
def preprocess_function(examples):
    return tokenizer(examples['text'], padding=True, truncation=True)

tokenized_train_dataset = train_dataset.map(preprocess_function, batched=True)
tokenized_eval_dataset = eval_dataset.map(preprocess_function, batched=True)
print("eval:",tokenized_eval_dataset)
print("train:",tokenized_train_dataset)
#%%
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_eval_dataset  # Add this line to include evaluation data
)

trainer.train()
#%%
trainer.evaluate()

# For prediction
def predict_category(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    print(outputs.logits)
    predictions = outputs.logits.argmax(-1)
    return predictions.item()

new_text = "cook delicious recipe ingredient  dessert cake "
category = predict_category(new_text)
print(f"Predicted category: {category}")