#Vishing Detection Project - Nabaha

This project is designed to detect vishing (voice phishing). The goal of the system is to raise awareness about fraudulent phone calls and demonstrate how artificial intelligence can be applied in cybersecurity.

The system takes in a spoken or written message and analyzes it to determine whether it is a legitimate call or a vishing attempt. The message is processed using natural language understanding tools and classified using a trained machine learning model.

##The project consists of three main files

###vishing_dataset.csv
This file contains a labeled dataset of Arabic phone call transcripts. Each row represents a single message or call transcript. The dataset includes features that indicate the presence of suspicious patterns, such as:
- Requesting a password or code
- Asking for personal or banking information
- Using threats or urgency
- Offering fake deals or money transfers

These labels help the model learn how vishing calls typically behave.

### vishing_classifier.pkl
This is a machine learning model that was trained using the vishing_dataset.csv file. It takes in Arabic messages (text) and predicts whether certain suspicious features are present. The model uses sentence embeddings from an Arabic BERT model to understand the meaning of the message.

The classifier was trained as a multilabel model, meaning it can detect more than one suspicious intent in the same message.

### vishing_detector_api.ipynb
This is a Google Colab notebook that allows the system to be run online using a simple API. It includes the following steps and features:

- Installs all required packages (including Whisper, FastAPI, BERT, etc.)
- Loads the trained classifier and sentence transformer encoder
- Loads the Whisper model to transcribe Arabic audio
- Starts a FastAPI web server to handle requests
- Opens a public URL using ngrok for testing
- Defines two API endpoints:
  - /analyze-text: Accepts a plain Arabic text message and returns predicted labels and confidence
  - /analyze-audio: Accepts an audio file, transcribes it using Whisper, then analyzes the result

This notebook allows anyone to interact with the model through a web API, making it easy to integrate with apps like Lovable or test it manually.

## How the system works

1. A message is submitted to the system, either as audio or plain text.
2. If it's audio, the Whisper model is used to transcribe the message to Arabic text.
3. The message is passed to the trained classifier.
4. The message is encoded using BERT to extract semantic meaning.
5. The classifier checks if the message contains any suspicious features and returns:
   - A list of the detected labels (like request for password, threat, etc.)
   - A confidence score

This output can be used to decide if the message is safe or potentially dangerous.

## Use cases

- Testing the system against real or synthetic call transcripts
- Integrating the API into awareness apps for cybersecurity
- Demonstrating how AI can be used to detect fraud and phishing in Arabic contexts

## Setup notes

- The notebook requires Google Colab to run and needs a few files to be uploaded:
  - vishing_classifier.pkl
  - vishing_dataset.csv
- You must also provide your ngrok token to generate the public API link
- The system runs in real-time and is accessible from the browser or other tools once ngrok is connected

## Final thoughts

This project highlights the importance of AI in digital fraud prevention. By focusing on Arabic language calls, it also shows how local linguistic and cultural factors play a role in cybersecurity solutions. The system is modular and can be improved further by refining the dataset or adding more advanced features.
