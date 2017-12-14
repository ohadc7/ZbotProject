import os
from collections import deque
#os.sys('ffmpeg -i 04.wav -af silencedetect=noise=0.0001 -f null -2  > vol.')


os.system('ffmpeg -i "audio/4.wav" -af silencedetect=noise=-30dB:d=0.5 -f null - 2> vol.txt')

with open('vol.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')

keyword = '[silencedetect'
befor_keyowrd, keyword, after_keyword = data.partition(keyword)

keyword='size'
befor_keyowrd, keyword, after_keyword = after_keyword.partition(keyword)



limit = 100
prev_items = deque(maxlen=limit)

# Open file and iterate over lines.
with open('vol.txt') as f:
    for line in f:
        # Add the line to the deque.
        prev_items.append(line)

        # If the current line is 'Alpha', we don't need to read any more.
        if line == 'Alpha':
           break

# Append prev_items to the results file.
with open('results.txt', 'a') as f:
    f.write('\n'.join(prev_items))