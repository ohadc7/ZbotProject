import os
from collections import deque
#os.sys('ffmpeg -i 04.wav -af silencedetect=noise=0.0001 -f null -2  > vol.')


os.system('ffmpeg -i "audio/4.wav" -af silencedetect=noise=-30dB:d=0.5 -f null - 2> vol.txt')

with open('vol.txt', 'r') as myfile:
    data=myfile.read()

keyword = '[silencedetect'
befor_keyowrd, keyword, after_keyword = data.partition(keyword)

keyword='size'
befor_keyowrd, keyword, after_keyword = after_keyword.partition(keyword)

print befor_keyowrd


# Append prev_items to the results file.
with open('results.txt', 'a') as f:
    f.write('\n'.join(prev_items))