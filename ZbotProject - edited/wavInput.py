import scipy.io.wavfile as wf
import numpy

from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "2021_20171127_142358_d.wav")

rate, data = wf.read(AUDIO_FILE)
# data0 is the data from channel 0.
data0 = data[:, 0]
data1 = data[:, 1]