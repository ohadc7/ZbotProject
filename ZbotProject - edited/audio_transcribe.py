#!/usr/bin/env python3

from __future__ import print_function

from pydub import AudioSegment

import speech_recognition as sr
import scipy.io.wavfile as wf
import numpy

import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence

#log = open("text.txt", "w")
import shutil
from shutil import rmtree
import os
from silence_detection import talking_times

UnseparatedWavFilesPath = "audio"

def invert_wav_to_flac(wavFile, flacFile):
    leftChunkFlacFile = open(flacFile, "w+")
    song = AudioSegment.from_wav(wavFile)
    song.export(flacFile, format="flac")
    return flacFile

def omit_extension(fileName, expectedExtension):
    extensionLength = len(expectedExtension)
    extension = file[-extensionLength:]
    if (extension != expectedExtension):
        raise NameError('The file ' + fileName + 'doesn\'t have ' + expectedExtension + ' extension.')
    filePathWithoutExtension = file[:-extensionLength]
    return filePathWithoutExtension


shutil.rmtree("temp_dir", True)
os.mkdir("temp_dir")

if(os.path.isdir(UnseparatedWavFilesPath) is not True):
    raise NameError('The directory ' + UnseparatedWavFilesPath + ' wasn\'t found. Please create this directory in the current location and put wav files in it.')

wavFilesList = os.listdir(UnseparatedWavFilesPath)
for file in wavFilesList:
    wavFileWithoutExtension = omit_extension(file, ".wav")

    LeftChannelFile = "temp_dir/" + wavFileWithoutExtension + "_left.wav"
    RightChannelFile = "temp_dir/" + wavFileWithoutExtension + "_right.wav"

    os.system('ffmpeg -i ' + UnseparatedWavFilesPath + '/' + file + ' -map_channel 0.0.0 ' + LeftChannelFile + ' -map_channel 0.0.1 ' + RightChannelFile)

    leftFlacFileName = "temp_dir/" + wavFileWithoutExtension + "_left_chunk.flac"
    rightFlacFileName = "temp_dir/" + wavFileWithoutExtension + "_right_chunk.flac"
    leftFlacFile = invert_wav_to_flac(LeftChannelFile, leftFlacFileName)
    rightFlacFile = invert_wav_to_flac(RightChannelFile, rightFlacFileName)

    left_times = talking_times(leftFlacFile)
    right_times = talking_times(rightFlacFile)

    talking_time_left = {}
    talking_time_right = {}

    first_talk_left = left_times.pop(0)
    first_talk_right = right_times.pop(0)
    counter = 0
    while(left_times != [] and right_times != []):
        if(first_talk_left < first_talk_right):
            # print("left: ")
            # print(first_talk_left)
            # print('ffmpeg -ss ' + str(first_talk_left[0] - 0.15) + ' -t ' +
            #           str(first_talk_left[1] - first_talk_left[0] + 0.15) +
            #           ' -i ' + leftFlacFileName + ' temp_dir/segment' + str(counter) + '_left.flac')
            os.system('ffmpeg -ss ' + str(first_talk_left[0] - 0.15) + ' -t ' +
                      str(first_talk_left[1] - first_talk_left[0] + 0.15) +
                      ' -i ' + leftFlacFileName + ' temp_dir/segment' + str(counter) + '_left.flac')
            counter = counter + 1
            if(left_times != []):
                first_talk_left = left_times.pop(0)

        else:
            # print("right: ")
            # print(first_talk_right)
            # print('ffmpeg -ss ' + str(first_talk_right[0] - 0.15) + ' -t ' +
            #           str(first_talk_right[1] - first_talk_right[0] + 0.15) +
            #           ' -i ' + rightFlacFileName + ' temp_dir/segment' + str(counter) + '_right.flac')
            os.system('ffmpeg -ss ' + str(first_talk_right[0] - 0.15) + ' -t ' +
                      str(first_talk_right[1] - first_talk_right[0] + 0.15) +
                      ' -i ' + rightFlacFileName + ' temp_dir/segment' + str(counter) + '_right.flac')
            counter = counter + 1
            if (right_times != []):
                first_talk_right = right_times.pop(0)

    if (first_talk_left < first_talk_right):
        # print("left: ")
        # print(first_talk_left)
        os.system('ffmpeg -ss ' + str(first_talk_left[0] - 0.15) + ' -t ' +
                  str(first_talk_left[1] - first_talk_left[0] + 0.15) +
                  ' -i ' + leftFlacFileName + ' temp_dir/segment' + str(counter) + '_left.flac')
        counter = counter + 1
        # print("right: ")
        # print(first_talk_right)
        os.system('ffmpeg -ss ' + str(first_talk_right[0] - 0.15) + ' -t ' +
                  str(first_talk_right[1] - first_talk_right[0] + 0.15) +
                  ' -i ' + rightFlacFileName + ' temp_dir/segment' + str(counter) + '_right.flac')
        counter = counter + 1
    else:
        # print("right: ")
        # print(first_talk_right)
        os.system('ffmpeg -ss ' + str(first_talk_right[0] - 0.15) + ' -t ' +
                  str(first_talk_right[1] - first_talk_right[0] + 0.15) +
                  ' -i ' + rightFlacFileName + ' temp_dir/segment' + str(counter) + '_right.flac')
        counter = counter + 1
        # print("left: ")
        # print(first_talk_left)
        os.system('ffmpeg -ss ' + str(first_talk_left[0] - 0.15) + ' -t ' +
                  str(first_talk_left[1] - first_talk_left[0] + 0.15) +
                  ' -i ' + leftFlacFileName + ' temp_dir/segment' + str(counter) + '_left.flac')
        counter = counter + 1

    while(left_times != []):
        first_talk_left = left_times.pop(0)
        os.system('ffmpeg -ss ' + str(first_talk_left[0] - 0.15) + ' -t ' +
                  str(first_talk_left[1] - first_talk_left[0] + 0.15) +
                  ' -i ' + leftFlacFileName + ' temp_dir/segment' + str(counter) + '_left.flac')
        counter = counter + 1

    while(right_times != []):
        first_talk_right = right_times.pop(0)
        os.system('ffmpeg -ss ' + str(first_talk_right[0] - 0.15) + ' -t ' +
                  str(first_talk_right[1] - first_talk_right[0] + 0.15) +
                  ' -i ' + rightFlacFileName + ' temp_dir/segment' + str(counter) + '_right.flac')
        counter = counter + 1



'''
    # use the audio file as the audio source
    # read the entire audio file

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`

        f = open('text.txt', 'w')
        r = sr.Recognizer()
        with sr.AudioFile(leftFlacFileName) as source:
            audio = r.record(source)

        f.write('\n' + r.recognize_google(audio).encode('utf8'))
        f.close()

        # print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

sound_file = AudioSegment.from_wav(wavFileWithoutExtension)
# must be silent for at least half a second
min_silence_len=2000,
# consider it silent if quieter than -16 dBFS
silence_thresh=-20
if (len(sys.argv) > 2):
    min_silence_len=int(sys.argv[2])
if (len(sys.argv) > 3):
    silence_thresh=int(sys.argv[3])



audio_chunks = split_on_silence(sound_file,
    # must be silent for at least half a second
    min_silence_len,

    # consider it silent if quieter than -16 dBFS
    silence_thresh
)
r = sr.Recognizer()

for i, chunk in enumerate(audio_chunks):
    #out_file = open("chunk{0}.wav".format(i), "r+")
    out_file = open("chunk.wav", "w+")
    #print
    #var = "exporting", out_file
    chunk.export(out_file, format="wav")
    from pydub import AudioSegment
    leftChunkFlacFile = open("chunk.flac", "w+")
    song = AudioSegment.from_wav("chunk.wav")
    song.export("chunk.flac", format="flac")
    with sr.AudioFile("chunk.flac") as source:
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
'''

