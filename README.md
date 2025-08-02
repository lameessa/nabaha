# Vishing Detection Project - Nabaha

This project is designed to detect vishing, which is a type of voice phishing where attackers attempt to extract sensitive information from victims through phone calls. 
The system was built using artificial intelligence tools to raise awareness about fraud and demonstrate how modern AI can help detect these cyberattacks.

## The project consists of three main files
### vishing_dataset.csv
This is a labeled dataset containing transcripts of Arabic phone calls. Each row represents a line of dialogue in a phone conversation, annotated with binary features (0 or 1) to indicate the presence of suspicious behavior. These features include:

- is_urgent: whether the caller creates urgency or pressure
- used_threat: whether the caller uses threats or intimidation
- good_offers: whether the caller offers fake deals or unrealistic promises
- request_money_transfer: whether the caller asks for a money transfer
- request_personal_info: whether the caller asks for personal information (like ID)
- request_banking_info: whether the caller asks for banking information
- request_passwords: whether the caller asks for a password
- request_code: whether the caller asks for a verification code
- is_vishing: the label that indicates whether the line is part of a vishing attack

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
  - /analyze-text: Accepts a plain Arabic text message and returns predicted labels and confidence (used to test the model)
  - /analyze-audio: Accepts an audio file, transcribes it using Whisper, then analyzes the result (used in the project frontend)

This notebook allows anyone to interact with the model through a web API, making it easy to integrate with apps like Lovable or test it manually.

### Integration with Lovable

The frontend of the project is built with Lovable and is available at:
https://preview--vishing-guard-scan.lovable.app/

The GitHub repository for the frontend is:
https://github.com/layanalnn/Nabaha-FrontEnd.git

#### To connect the backend API with Lovable:
- Make sure the notebook is running and the public ngrok URL is active.
- Copy the link generated in the notebook (it ends with .ngrok-free.app/analyze-audio).
- Update Lovable’s record button to send the audio to the /analyze-audio endpoint.
- The audio should be sent as multipart/form-data with the field name file.

## How the system works

1. The system records a phone call as an audio file.
2. The Whisper model is used to transcribe the audio message to Arabic text.
3. The message is passed to the trained classifier.
4. The message is encoded using BERT to extract semantic meaning.
5. The classifier checks if the message contains any suspicious features and returns:
   - A list of the detected labels (only if vishing is detected)
   - A confidence score

This output can be used to decide if the message is safe or potentially dangerous.

## Use cases

- Testing the system against real or synthetic call transcripts
- Integrating the API into awareness apps for cybersecurity
- Demonstrating how AI can be used to detect fraud and phishing in Arabic contexts

## Setup notes

- Run the notebook on Google Colab.
- Upload vishing_classifier.pkl before starting.
- Ngrok token is already provided.
- After running, copy the ngrok API link shown in the output.
- Paste that link in Lovable (only 5 edits allowed per day).

## Final thoughts

This project highlights the importance of AI in digital fraud prevention. By focusing on Arabic language calls, it also shows how local linguistic and cultural factors play a role in cybersecurity solutions. The system is modular and can be improved further by refining the dataset or adding more advanced features.
