import os
from collections import deque
#os.sys('ffmpeg -i 04.wav -af silencedetect=noise=0.0001 -f null -2  > vol.')

def silence_times(path):
    os.system('ffmpeg -i ' + path + ' -af silencedetect=noise=-30dB:d=0.5 -f null - 2> vol.txt')

    with open('vol.txt', 'r') as myfile:
        data=myfile.read()

    keyword = '[silencedetect'
    befor_keyowrd, keyword, after_keyword = data.partition(keyword)

    keyword='size'
    befor_keyowrd, keyword, after_keyword = after_keyword.partition(keyword)

    silences_times = {}


    #befor_keyowrd, keyword, after_keyword = after_keyword.partition("silence_start: ")

    while (befor_keyowrd.find("silence_duration: ") != -1):
        start = befor_keyowrd.find("silence_start: ") + 15
        end = befor_keyowrd.find("\n")
        start_time = float(befor_keyowrd[start:end])
        #print start_time
        befor_keyowrd = befor_keyowrd[start + 8:]
        start = befor_keyowrd.find("silence_duration: ") + 18
        end = befor_keyowrd.find("\n")
        duration_time = float(befor_keyowrd[start:end])
        #print duration_time
        silences_times[start_time] = duration_time
        befor_keyowrd = befor_keyowrd[start + 8:]

    sort = sorted(silences_times.items())
    #talking_time ={}
    #silence = sort.pop(0)
    #talking_start = float(silence.count(0) + silence.index(1))
    #while(sort != []):
        #print("debug::::::::::::::::")
        #print silence
        #print(silence)
        #talking_start = silence.index(0) + silence.index(1)
        #silence = sort.pop(0)
        #talking_end = silence.index(0)
        #print("talk start" + talking_start)
        #print("talk end" + talking_end)


    print sort
    return sort

#[silencedetect

#print befor_keyowrd


# Append prev_items to the results file.
#with open('results.txt', 'a') as f:
#    f.write('\n'.join(prev_items))