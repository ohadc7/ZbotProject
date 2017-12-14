import os
from collections import deque
#os.sys('ffmpeg -i 04.wav -af silencedetect=noise=0.0001 -f null -2  > vol.')
import re

os.system('ffmpeg -i "audio/4.wav" -af silencedetect=noise=-30dB:d=0.5 -f null - 2> vol.txt')

with open('vol.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')

keyword = '[silencedetect'
befor_keyowrd, keyword, after_keyword = data.partition(keyword)

keyword='size'
befor_keyowrd, keyword, after_keyword = after_keyword.partition(keyword)

for line in befor_keyowrd:
    if re.match("(.*)(L|l)ove(.*)", line):
        print line,
