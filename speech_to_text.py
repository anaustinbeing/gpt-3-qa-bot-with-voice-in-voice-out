import pyaudio
import vosk
import json
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = "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"

start_sequence = "\nA:"
restart_sequence = "\n\nQ: "

all_prompts = ''

# Initialize PyAudio
p = pyaudio.PyAudio()

# Set parameters for audio input
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

start_sequence = "\nA:"
restart_sequence = "\n\nQ: "
all_prompts = ''

# Create an instance of Vosk recognizer
model = vosk.Model(model_name="vosk-model-en-us-0.42-gigaspeech")
recognizer = vosk.KaldiRecognizer(model, RATE)

# Open the microphone for audio input
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Start recording
def start_recording():
    print("Listening...")

    sentence_complete = False
    transcript = ""

    while not sentence_complete:
        data = stream.read(CHUNK)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result["text"]
            transcript += text
            return transcript

# Stop recording
def stop_recording():
    print('Stopping...')
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('Stopped listening.')

def transcribe():
    print('Transcribing..')
    sentence_complete = False
    transcript = ""

    while not sentence_complete:
        data = stream.read(CHUNK)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result["text"]
            transcript += text
            break
    all_prompts = restart_sequence + question

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
        answer = 'Your question is not clear. Please try again.'
    return [transcript, answer]