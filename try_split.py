import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence


sound_file = AudioSegment.from_wav(sys.argv[1])
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

for i, chunk in enumerate(audio_chunks):

    out_file = ".//splitAudio//chunk{0}.wav".format(i)
    print "exporting", out_file
    chunk.export(out_file, format="wav")
