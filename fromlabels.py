#import mir_eval
import librosa
import sys

songpath = sys.argv[1]

print('.'.join(songpath.split('.')[:-1])+'.txt')

# Lets parse those audacity Label files
money,sample_rate = librosa.load(songpath,sr=None)

# make initial whole-song tempo guess, to feed into segment tempos
avg_tempo = librosa.feature.tempo(y=money,sr=sample_rate)[0]

print(f'initial tempo guess: {avg_tempo}')

with open('.'.join(songpath.split('.')[:-1])+'.txt', 'r') as f:
    lines = [l.strip().split('\t') for l in f.readlines()]

# [START, STOP, LABEL]

lines = [[float(l[0]), float(l[1]), l[2]] for l in lines]

# get beats from song

# turn that into a list of sections
# [ {start:time, name:"name"} ]
# if two are within label_radius, use the beat in the middle/closest to them as the time
# if two are outside of label_radius, insert another section in between

label_radius = 1 # second
sections = []

def addSec(l, start, end, name):
    

    startSample = int(start*sample_rate)
    endSample = int(end*sample_rate)

    audio_slice = money[ startSample:endSample ]

    tempo, beats = librosa.beat.beat_track(y=audio_slice, sr=sample_rate, 
                                           start_bpm=avg_tempo, tightness=100)
    beat_times = librosa.frames_to_time(beats)

    # get dumb beats by doing time(min) * bpm
    dumb_beats = (end - start) * avg_tempo / 60
    smart_beats = len(beat_times)
    
    d = {'start':start, 'end':end, 'name':name, 
         'tempo':tempo, 'beat_times':beat_times,
         'slice':audio_slice, 'smart_beats':smart_beats, 'dumb_beats':dumb_beats}

    l.append(d)

if lines[0][0] > label_radius:
    addSec(0, lines[0][0], 'PRE-INTRO')

# for each song
for line in lines:
    # check the start against the previous start
    if (len(sections) > 0) and (line[0] - sections[-1]['end']) > label_radius:
        addSec(sections, sections[-1]['end'], line[0], 'UNKNOWN')
    
    # create one for this song
    addSec(sections, line[0], line[1], line[2])

x = 0

#y_tone = mir_eval.sonify.clicks(sections[x]['beat_times'],sample_rate,length=len(sections[x]['slice']))

def groupBeats(time_sig, smart_beats, dumb_beats):
    #b = (smart_beats + dumb_beats) / 2
    b = dumb_beats

    groups = [x*time_sig for x in [8, 4, 2, 1]]

    for g in groups:
        rem = b % g
        if rem > g/2:
            rem = g - rem
        if rem < time_sig*0.6:
            return g/time_sig, round(b/g,2)

    return None

delimeter = '\t'

print(delimeter.join(['SMART', 'DUMB', 'MEASURE', 'SECTION', 'LABEL']))

for s in sections:
    x,y = groupBeats(4, s['smart_beats'], s['dumb_beats'])
    print(delimeter.join([str(s['smart_beats']), str(round(s['dumb_beats'],3)), str(x), str(y), s['name']]))


