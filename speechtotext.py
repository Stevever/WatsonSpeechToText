from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname
import os
import json

speech_to_text = SpeechToTextV1(
    iam_apikey='FMdj05bLeFKPX95Ve-wStDFWYFXXuqZDXzLHsT4paUHh',
    url='https://stream.watsonplatform.net/speech-to-text/api'
)

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        #print(json.dumps(data, indent=2))
        transcript = ''.join(result['alternatives'][0]['transcript']
                             for result in data['results'])
        print(transcript)

        word_count = len(transcript.split())
        weighted_confidence = 0
        for result in data['results']:
            text_len = len(result['alternatives'][0]['transcript'].split())
            weighted_confidence += result['alternatives'][0]['confidence'] * text_len / word_count
        print(weighted_confidence)

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

myRecognizeCallback = MyRecognizeCallback()

for file in os.listdir(join(dirname(__file__), './resources')):
    with open(join(dirname(__file__), './resources', file), 'rb') as audio_file:
        print(file)
        audio_source = AudioSource(audio_file)
        speech_to_text.recognize_using_websocket(
            audio=audio_source,
            content_type='audio/mp3',
            recognize_callback=myRecognizeCallback,
            model='en-US_BroadbandModel')
