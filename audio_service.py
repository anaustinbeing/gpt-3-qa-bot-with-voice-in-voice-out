from boto3 import Session
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir


class AudioService:
    def __init__(self):
        self.client = boto3.client('polly')

    def generate_audio(self, text):
        try:
            # Request speech synthesis
            response = self.client.synthesize_speech(Text=text, OutputFormat="mp3",
                                                VoiceId="Joanna")
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

        # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.dirname(os.path.realpath(__file__)) + '\speech.mp3'
                try:
                    # Open a file for writing the output as a binary stream
                    with open("speech.mp3", "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        # Play the audio using the platform's default player
        if sys.platform == "win32":
            os.startfile(output)
        else:
            # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, output])
