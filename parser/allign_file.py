import guitarpro as gp
from allign_tracks import get_guitar_bass, allign
from itertools import product

file_name = '/Users/talbaumel/Dropbox/Guitar Pro Tabs - 55000/B/Bad Religion/Bad Religion - When_.gp3'

song = gp.parse(file_name)
for guitar, bass in product(*get_guitar_bass(song)):
    input, output = allign(guitar, bass)