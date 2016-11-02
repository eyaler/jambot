from parser2 import parse_gp_file, universal_sample_rate
from util import song_player
from time import sleep


player = song_player(tempo=universal_sample_rate)
#file_name = '/Users/talbaumel/Dropbox/Guitar Pro Tabs - 55000/B/Beatles (The)/Beatles (The) - Rocky Raccoon.gp3'
file_name = '/Users/talbaumel/Dropbox/Simon & Garfunkel - A Hazy Shade Of Winter0'
for line in open(file_name):

    s0, s1 = line.strip().split(',')
    player.play_notes(s0,  pitch_offset=-12, track=0)
    player.play_notes(s1,  pitch_offset=+12, track=1)
    sleep(universal_sample_rate/2500.)
    #player.play_song([s for s in song], volume=(127,104), pitch_offset=(-12,12))