# gpt-3-qa-bot-with-voice-in-voice-out

This is a GPT-3 based question answering bot with voice input and voice output. This works on terminal. You can execute by running question_answering_bot.py after installing necessary packages (i.e, run requirements.txt first). Make sure you also paste the api key from openai in the config.py file.

## What is behind?

**openai**: Use the openai library to integrate OpenAI's GPT model for generating conversational responses in the chatbot.

**pyaudio**: Employ the pyaudio library to capture audio input from the user's microphone and to play audio responses.

**vosk**: Utilize the vosk library to perform real-time speech recognition and convert user voice input into text.

**boto3**: Leverage the boto3 library to interact with AWS services for managing cloud resources used in the chatbot (Amazon Polly, in this case).

**Amazon polly**: Implement the amazon polly service via boto3 to convert the chatbot's text responses into lifelike speech.

Enjoy chatting!
