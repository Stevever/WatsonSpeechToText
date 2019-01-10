from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname
import os
import json
import difflib

speech_to_text = SpeechToTextV1(
    iam_apikey='FMdj05bLeFKPX95Ve-wStDFWYFXXuqZDXzLHsT4paUHh',
    url='https://stream.watsonplatform.net/speech-to-text/api'
)

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        transcript = ''.join(result['alternatives'][0]['transcript']
                             for result in data['results'])
        print(transcript, file=open("output.txt", "a"))

        print(difflib.SequenceMatcher(None, transcript.lower(), original_text).ratio(), file=open("output.txt", "a"))

        word_count = len(transcript.split())
        weighted_confidence = 0
        for result in data['results']:
            text_len = len(result['alternatives'][0]['transcript'].split())
            weighted_confidence += result['alternatives'][0]['confidence'] * text_len / word_count
        print(weighted_confidence, file=open("output.txt", "a"))

    def on_error(self, error):
        print('Error received: {}'.format(error), file=open("output.txt", "a"))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error), file=open("output.txt", "a"))

myRecognizeCallback = MyRecognizeCallback()
original_text = ("please call stella ask her to bring these things with her "
                 "from the store six spoons of fresh snow peas five thick "
                 "slabs of blue cheese and maybe a snack for her brother bob "
                 "we also need a small plastic snake and a big toy frog for "
                 "the kids she can scoop these things into three red bags and "
                 "we will go meet her wednesday at the train station "
                )

for file in os.listdir(join(dirname(__file__), './resources')):
    with open(join(dirname(__file__), './resources', file), 'rb') as audio_file:
        print(file, file=open("output.txt", "a"))
        audio_source = AudioSource(audio_file)
        speech_to_text.recognize_using_websocket(
            audio=audio_source,
            content_type='audio/mp3',
            recognize_callback=myRecognizeCallback,
            model='en-US_BroadbandModel')
