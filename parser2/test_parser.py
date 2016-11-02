from parser2 import parse_gp_file, universal_sample_rate
from utils import song_player
from time import sleep


player = song_player(tempo=universal_sample_rate)
#file_name = '/Users/talbaumel/Dropbox/Guitar Pro Tabs - 55000/B/Beatles (The)/Beatles (The) - Rocky Raccoon.gp3'
file_name = '/Users/talbaumel/Dropbox/Ramones (The) - BlitzKrieg Bop (2)0'
for guitar, bass in parse_gp_file(file_name):
    print 'part'
    song = zip(bass, guitar)
    for s0, s1 in song:
        print s0, s1
        player.play_notes(s0,  pitch_offset=-12, track=0)
        player.play_notes(s1,  pitch_offset=+12, track=1)
        sleep(universal_sample_rate/2000.)
    #player.play_song([s for s in song], volume=(127,104), pitch_offset=(-12,12))