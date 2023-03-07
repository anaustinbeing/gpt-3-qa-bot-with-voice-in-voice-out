import os
import time
import openai
from speech_to_text import start_recording, stop_recording
from audio_service import AudioService
from config import api_key

audio_service = AudioService()

# Load your API key from an environment variable or secret management service
openai.api_key = api_key

start_sequence = "\nA:"
restart_sequence = "\n\nQ: "
all_prompts = ''

print('\nASK ME FACTS!')
print('To exit the session, say "exit"')
try:
    while True:
        # question = input('Enter your question: ')
        print()
        question = start_recording()
        if question.strip().lower() == "exit":
            break
        if question:
            print('You asked: ' + question)
            all_prompts += restart_sequence + question

            response = openai.Completion.create(
            model="text-davinci-003",
            prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\"" + all_prompts + "\nA:",
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
            )
            answer = response['choices'][0]['text']
            all_prompts += start_sequence + answer
            if answer.strip().lower() == 'unknown':
                print('Your question is not clear. Please try again.')
                continue
            print(answer)
            audio_service.generate_audio(answer)
            time.sleep(5)
except Exception as e:
    print('Closing the session...')
    print(e)
    stop_recording()
print('Closing the session...')
stop_recording()