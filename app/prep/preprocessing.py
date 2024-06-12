# app\prep\preprocessing.py
import re
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Load your pre-trained TensorFlow model
model = tf.keras.models.load_model('app/prep/model/onsite_request_model.h5')

# Load tokenizer from pickle file
try:
    with open('app/prep/model/tokenizer_config.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
except FileNotFoundError:
    raise FileNotFoundError("Tokenizer file 'tokenizer_config.pkl' not found.")
except pickle.UnpicklingError:
    raise ValueError("Unable to unpickle tokenizer from 'tokenizer_config.pkl'.")

# Set the tokenizer's oov_token
tokenizer.oov_token = 'none'

# Example sequence length, adjust this to match your model's requirements
SEQUENCE_LENGTH = 200

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text, re.I|re.A)
    text = text.lower()
    text = text.strip()
    return text

def preprocess_message(message):
    # Preprocess the text
    message = preprocess_text(message)
    # Tokenize the message
    message_seq = tokenizer.texts_to_sequences([message])
    # Pad the message
    message_pad = pad_sequences(message_seq, maxlen=SEQUENCE_LENGTH, padding='post')
    return message_pad

def classify_message(message):
    # Preprocess message
    processed_message = preprocess_message(message)
    prediction = model.predict(processed_message)
    return 'onsite' if prediction[0][0] > 0.5 else 'not onsite'

if __name__ == "__main__":
    test_message = "there is a leeakage in toilet, please send someone to fix it" #"The light bulb in the bathroom is not working. Can you send someone to fix it?"
    classification = classify_message(test_message)
    print("Classification:", classification)
