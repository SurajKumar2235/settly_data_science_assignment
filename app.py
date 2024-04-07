from fastapi import FastAPI
from sklearn.preprocessing import LabelEncoder
import pickle
import tensorflow as tf
import numpy as np
import keras
import re
from keras.models import load_model

from keras.preprocessing.sequence import pad_sequences
# Load the LabelEncoder
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)



# Load the saved model
model = load_model("model.keras")

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
app = FastAPI()

@app.get("/pos/")
async def predict_internal_status(user_input: str):
    # Tokenize the user input
    user_input=user_input.lower()
    user_input=re.sub(r'[^\w\s]', '', user_input)

    
    user_input_sequence = tokenizer.texts_to_sequences([user_input])
    # Pad sequences to the same length as training data
    user_input_sequence_padded = pad_sequences(user_input_sequence, maxlen=130)

    # Make predictions
    predictions = model.predict(user_input_sequence_padded)
    # Get the predicted class (internal status)
    predicted_class_index = np.argmax(predictions)
    print('probability of current prediction------>',np.max(predictions))
    # Inverse transform to get the actual value from label encoding
    predicted_class = label_encoder.inverse_transform([predicted_class_index])

    return {"predicted_internal_status": predicted_class[0]}
