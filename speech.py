#!/usr/bin/python

import pyaudio
import wave
import sys
import urllib2
import json
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')                                     
wf.setnchannels(CHANNELS)                                                      
wf.setsampwidth(p.get_sample_size(FORMAT))                                     
wf.setframerate(RATE)                                                          
wf.writeframes(b''.join(frames))                                               
wf.close()  

out = os.system("flac -f " + WAVE_OUTPUT_FILENAME)

f = open("output.flac")
data = f.read()
f.close()

req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=pt-BR', data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})

ret = urllib2.urlopen(req)

#print ret.read()
text = json.loads(ret.read())['hypotheses'][0]['utterance']
print text
