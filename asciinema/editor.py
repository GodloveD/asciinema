import sys
import re
from itertools import accumulate
from .asciicast import Asciicast

def __parse_clip__(asciicast, clip_spec=None):

    if clip_spec is None: clip_spec = ''
    'parse clip_spec to see if it is time or frames'
    ''' Do error checking
    : = everything
    5:100 = frame 5 to 100
    5: = frame 5 to end
    :100 = frame start to 100
    0:10, =  10 seconds to end 
    ,0:30 =  start to 30 seconds
    1:20:20.511,1:21:0.5 = hr:minute:seconds.fraction to hr:minute:seconds.fraction
    1:00,2 = illegal. one minute to 2 seconds 
    if start >= stop:
        print('NO!')
        return 1
    '''

    start = 0; fin = 1
    time = list(accumulate([a[0] for a in asciicast.stdout.frames]))

    if ',' in clip_spec:
        clip_spec = re.split(',', clip_spec)
        clip_spec = [__parse_time__(a) for a in clip_spec]

        if isinstance(clip_spec[start], float):
            clip_spec[start] = next(i for i,t in enumerate(time) if t >= clip_spec[start]) +1
        if isinstance(clip_spec[fin], float):
            clip_spec[fin] = next(i for i,t in enumerate(time) if t > clip_spec[fin])

        clip_spec = "%s:%s"%(str(clip_spec[start]), str(clip_spec[fin]))

    clip_spec = re.split(':', clip_spec)

    if clip_spec[start] is '':  clip_spec[start] = start
    
    frameN = len(asciicast.stdout.frames) - 1
    if len(clip_spec) == 1: clip_spec.append(frameN) 
    if clip_spec[fin] is '':  clip_spec[fin] = frameN

    clip = slice(int(clip_spec[start]), int(clip_spec[fin]))
    return clip


def new_max(asciicast, max_time, clip=None):

    clip = __parse_clip__(asciicast, clip)

    diff = 0
    for this_echo in asciicast.stdout.frames[clip]:

        this_pause = this_echo[0]
        if this_pause > max_time:
            this_echo[0] = max_time
            diff = diff + this_pause - max_time
            
    asciicast.duration = asciicast.duration - diff
    return asciicast


def new_min(asciicast, min_time, clip=None):

    clip = __parse_clip__(asciicast, clip)

    diff = 0
    for this_echo in asciicast.stdout.frames[clip]:

        this_pause = this_echo[0]
        if this_pause < min_time:
            this_echo[0] = min_time
            diff = diff + min_time - this_pause
            
    asciicast.duration = asciicast.duration + diff
    return asciicast


def __parse_time__(timestring):

    match = re.split(":", timestring)

    if len(match) == 3:
        hr = match[0]; mn = match[1]; sc = match[2]
    elif len(match) == 2:
        hr = 0; mn = match[0]; sc = match[1]
    elif len(match) == 1:
        hr = 0; mn = 0; sc = match[0]
    else:
        'Error bad clip spec'

    if sc is '': return ''
    seconds = float(hr)*3600 + float(mn)*60 + float(sc)
    return seconds

