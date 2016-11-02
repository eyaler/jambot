from __future__ import division
import csv
import numpy as np
import mido
from mido import Message
import time
from queue import Queue
from threading import Thread
from config import *
#mido.set_backend('mido.backends.rtmidi')

key = 48


def one_hot(inp):
    out = np.zeros((len(inp), states))
    if inp is not None:
        for i,c in enumerate(inp):
            if c=='b':
                out[i,0] = 1
            elif c=='i':
                out[i,1] = 1
            elif c=='o':
                out[i,2] = 1
            else:
                raise TypeError
    return out

def load_song(filename):
    with open(filename) as f:
        rows = list(csv.reader(f))
        new_rows0 = []
        new_rows1 = []
        for row in rows:
            if len(row)>1:
                new_rows0.append(one_hot(row[0]))
                new_rows1.append(one_hot(row[1]))
        return np.asarray(new_rows0), np.asarray(new_rows1)

def index2bio(x):
    s = ''
    for i in x:
        if i == 0:
            s += 'b'
        elif i == 1:
            s += 'i'
        elif i == 2:
            s += 'o'
        else:
            raise TypeError
    return s

class song_player():
    def __init__(self, tempo, out_portname=None):
        self.state = [[False]*octave_len, [False]*octave_len]
        self.tempo = tempo/1000.
        self.key = key
        self.outport = mido.open_output(out_portname, autoreset=True)

    def play_song(self, lines, volume=(127,127), pitch_offset=(0,0)):
        for line in lines:
            time.sleep(self.tempo)
            if isinstance(line,list) or isinstance(line,tuple):
                self.play_notes(line[0], volume=volume[0], pitch_offset=pitch_offset[0], track=0)
                self.play_notes(line[1], volume=volume[1], pitch_offset=pitch_offset[1], track=1)
            else:
                self.play_notes(line, volume=volume[0], pitch_offset=pitch_offset[0])

    def play_notes(self, line, volume=127, pitch_offset=0, track=0):
        for i, c in enumerate(line):
            if c == 'b' or (not self.state[track][i] and c=='i'):
                m = Message('note_off', note=self.key + i + pitch_offset)
                self.outport.send(m)
                m = Message('note_on', note=self.key + i + pitch_offset, velocity=volume)
                self.outport.send(m)
                self.state[track][i] = True
            elif self.state[track][i] and c == 'o':
                m = Message('note_off', note=self.key + i + pitch_offset)
                self.outport.send(m)
                self.state[track][i] = False


def listener(q, in_portname=None):
    with mido.open_input(in_portname) as in_port:
        for message in in_port:
            q.put(message)


def get_bio(in_portname=None):
    q = Queue()
    t1 = Thread(target=listener, args=(q, in_portname))
    t1.start()

    state = ['o'] * octave_len
    while True:

        for i, c in enumerate(state):
            if c == 'b':
                state[i] = 'i'
            if c == 's':
                state[i] = 'o'

        while not q.empty():
            message = q.get()

            type = message.type == 'note_on'
            note = (message.note-key)%octave_len
            if type:
                state[note] = 'b'
            elif state[note] == 'b':
                state[note] = 's'
            else:
                state[note] = 'o'
        yield (''.join(state)).replace('s','b')


if __name__ == '__main__':
    for state in get_bio():
        print (state)