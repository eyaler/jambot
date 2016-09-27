import guitarpro as gp
import os, sys
from itertools import product
gp_folder = '/Users/talbaumel/Dropbox/Guitar Pro Tabs - 55000/'
song_key=0

def get_dirs(path):
    for file_or_dir in os.listdir(path):
        if os.path.isdir(path+file_or_dir):
            yield path+file_or_dir+'/'


def get_guitar_bass(song):
    guitars = []
    basses = []
    for track in song.tracks:
        if 'guitar' in track.name.lower():
            guitars.append(track)
        if 'bass' in track.name.lower():
            basses.append(track)
    return guitars, basses


letter_to_tav = {'c':0, 'c#':1, 'd':2, 'd#':3, 'e':4, 'f':5, 'f#':6, 'g':7, 'g#':8, 'a':9, 'a#':10, 'b':11}
def get_tav(string, press):
    string = str(string).lower()[:-1]
    return (letter_to_tav[string]+press - song_key)%12


def get_notes(track):
    notes = []
    for measure in track.measures:
        for voice in measure.voices:
            for beat in voice.beats:
                start = beat.start
                duration = beat.duration.time
                for note in beat.notes:
                    string = track.strings[note.string-1]
                    tav = get_tav(string, note.value)
                    notes.append({'note': tav, 'start': start, 'duration': duration})
    return notes


def analyze(notes):
    start = sys.maxint
    step = sys.maxint
    end = 0
    for n1, n2 in zip(notes[:-1],notes[1:]):
        start_temp = min(start, n1['start'])
        step_temp = min(step, n1['duration'], abs(n2['start']-n1['start']))
        if step_temp > 0:
            start = start_temp
            step = step_temp
        end = max(end, n2['start']+n2['duration'], n1['start']+n1['duration'])
    print step
    return start, step, end


def to_vector(notes, start, end, step):
    vector = []
    for _ in xrange(1+(end-start)/step):
        vector.append([])
        for _ in xrange(12):
            vector[-1].append('o')

    for note in notes:
        start_of_note_index = (note['start']-start)/step
        end_of_note_index = (note['start']+note['duration']-start)/step
        note = note['note']
        note_list = vector[start_of_note_index]
        note_list[note] = 'b'
        for i in range(start_of_note_index+1, end_of_note_index):
            vector[i][note] = 'i'

    return vector


def allign(guitar, bass):
    guitar_notes = get_notes(guitar)
    bass_notes = get_notes(bass)
    start, step, end = analyze(guitar_notes+bass_notes)

    input = to_vector(bass_notes, start, end, step)
    output = to_vector(guitar_notes, start, end, step)

    return input, output



def main():
    count = 0
    #skip = True
    for letter in get_dirs(gp_folder):
        for band in get_dirs(letter):
            for file_name in os.listdir(band):
                if file_name.startswith('.'):
                    continue

                file_name = band + file_name
                #if file_name == '/Users/talbaumel/Dropbox/Guitar Pro Tabs - 55000/D/Dissection/Dissection - Mistress Of The Bleeding Sorrow.gp4':
                #    skip = False
                #if skip:
                #    continue

                print file_name
                song = gp.parse(file_name)
                song_key = letter_to_tav[song.key.name[0].lower()]
                if song.key.name.endswith('p'):
                    song_key = (song_key + 1)%12
                if song.key.name.endswith('t'):
                    song_key = (song_key - 1)%12
                for guitar, bass in product(*get_guitar_bass(song)):
                    input, output = allign(guitar, bass)
                    with open('data/'+file_name.split('/')[-1]+str(count), 'w') as fp:
                        count+=1
                        for i, o in zip(input, output):
                            fp.write(''.join(i)+','+''.join(o)+'\n')
if __name__ == '__main__':
    main()