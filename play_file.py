from __future__ import division
from util import song_player
import csv

test_filename = 'd:/data/jambot/Ramones (The) - Blitzkrieg Bop (4).gp333532'

player = song_player(tempo=200)

with open(test_filename) as f:
    song = list(csv.reader(f))
player.play_song([s for s in song], volume=(127,104), pitch_offset=(0,12))
