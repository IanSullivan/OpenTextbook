from comtypes.client import CreateObject
import librosa
from comtypes.gen import SpeechLib
import html
from google.cloud import texttospeech as tts
import os
engine = CreateObject("SAPI.SpVoice")
stream = CreateObject("SAPI.SpFileStream")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\Users\\Donna\\PycharmProjects\\Intellegence\\gcloudKey.json"

client = tts.TextToSpeechClient()

def textToSpeech(text, index):

    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        name="en-AU-Neural2-A",
        language_code="en-AU", ssml_gender=tts.SsmlVoiceGender.FEMALE
    )

    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    outfile = "audio/" + str(index) + ".mp3"

    # The response's audio_content is binary.
    with open(outfile, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
    # outfile = "audio/" + str(index) + ".mp3"
    # stream.Open(outfile, SpeechLib.SSFMCreateForWrite)
    # engine.AudioOutputStream = stream
    # engine.speak(text)
    # stream.Close()
    # duration = librosa.get_duration(filename=outfile)
    # return duration


if __name__ == '__main__':
    textToSpeech("hey yall whats going in?", 0)

def text_to_ssml(inputfile):
    with open(inputfile, "r") as f:
        raw_lines = f.read()

    escaped_lines = html.escape(raw_lines)
    ssml = "<speak>{}</speak>".format(
        escaped_lines.replace("\n", '\n<break time="2s"/>')
    )
    return ssml

# text = """Here are <say-as interpret-as="characters">SSML</say-as> samples.
#   I can pause <break time="3s"/>.
#   I can play a sound"""
#
# # ssml = text_to_ssml(text)
# ssml = """
# <speak>123 Street Ln, Small Town, IL 12345 USA
# <break time="2s"/>1 Jenny St &amp; Number St, Tutone City, CA 86753
# <break time="2s"/>1 Piazza del Fibonacci, 12358 Pisa, Italy
# <break time="2s"/></speak>
# """
# print(ssml)
