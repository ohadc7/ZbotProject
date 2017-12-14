import os
import speech_recognition as sr

os.system('ffmpeg -i audio/4.wav -map_channel 0.0.0 audio/left4.wav -map_channel 0.0.1 audio/right4.wav')
from pydub import AudioSegment
chunkFile = open("audio/chunk.flac", "w+")
song = AudioSegment.from_wav("audio/left4.wav")
song.export("audio/chunk.flac", format="flac")
r = sr.Recognizer()
with sr.AudioFile("audio/chunk.flac") as source:
    audio = r.record(source)

    # use the audio file as the audio source
    # read the entire audio file

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`

    f = open('text.txt', 'w')

    f.write('\n' + r.recognize_google(audio).encode('utf8'))
    f.close()

    # print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

