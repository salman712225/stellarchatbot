import json
import random
import nltk
from nltk.stem import WordNetLemmatizer
import streamlit as st
import pandas as pd
from datetime import datetime

nltk.download('punkt')
nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents from the JSON file
with open('intents.json') as json_data:
    intents = json.load(json_data)

# Prepare patterns and responses
patterns = []
responses = []
tags = []

for intent in intents:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        responses.append(intent['responses'])
        tags.append(intent['tag'])

# Function to lemmatize words
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Function to classify the sentence
def classify_sentence(sentence):
    words = clean_up_sentence(sentence)
    # For simplicity, we are matching patterns directly
    for i, pattern in enumerate(patterns):
        for word in words:
            if word.lower() in pattern.lower():
                return tags[i]
    return "default"

# Function to handle responses
def get_response(tag):
    for intent in intents:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "Sorry, I didn't understand that."

# Streamlit app setup
st.title('Stellar Chatbot')
st.image('chatbot.png', width=150)
st.write("Welcome! How can I assist you with our services today?")

# Conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

def update_chat_history(user_input, bot_response):
    st.session_state.history.append({"user": user_input, "bot": bot_response})
    # Save the chat history to a CSV file
    chat_log = pd.DataFrame(st.session_state.history)
    chat_log.to_csv("chat_log.csv", index=False)

# Chatbot interaction
user_input = st.text_input("You: ")

if user_input:
    tag = classify_sentence(user_input)
    bot_response = get_response(tag)
    update_chat_history(user_input, bot_response)
    
    st.write("Bot: ", bot_response)
    
    # Display chat history
    for chat in st.session_state.history:
        st.write(f"You: {chat['user']}")
        st.write(f"Bot: {chat['bot']}")

