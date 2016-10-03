import guitarpro as gp
from itertools import product
from config import *


letter_to_tav = {'c':0, 'c#':1, 'd':2, 'd#':3, 'e':4, 'f':5, 'f#':6, 'g':7, 'g#':8, 'a':9, 'a#':10, 'b':11}
def get_tav(string, press):
    string = str(string).lower()[:-1]
    return (letter_to_tav[string]+press)%12


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


def get_guitar_bass(song):
    guitars = []
    basses = []
    for track in song.tracks:
        track_name = track.name.lower()
        if 'guitar' in track_name:
            guitars.append(track)
        if 'bass' in track_name:
            basses.append(track)
    return guitars, basses


def get_length(notes):
    return max(map(lambda note: note['start']+note['duration'], notes))


def to_vector(notes, length):
    vector = []
    for _ in xrange(1+(length)/universal_sample_rate):
        vector.append([])
        for _ in xrange(12):
            vector[-1].append('o')
    for note in notes:
        start_of_note_index = int(round(note['start']/universal_sample_rate))
        end_of_note_index = int(round((note['start']+note['duration'])/universal_sample_rate))
        note = note['note']
        note_list = vector[start_of_note_index]
        note_list[note] = 'b'
        for i in range(start_of_note_index+1, end_of_note_index):
            vector[i][note] = 'i'
    return map(lambda l: ''.join(l), vector)


def trim_start(guitar_vector, bass_vector):
    found_guitar = False
    found_bass = False
    for i, parts in enumerate(zip(guitar_vector, bass_vector)):
        if found_bass and found_guitar:
            cut = max(0, i-1)
            return guitar_vector[cut:], bass_vector[cut:]
        if not parts[0] == 'o'*12:
            found_guitar = True
        if not parts[1] == 'o'*12:
            found_bass = True
    return [], []


def trim_end(guitar_vector, bass_vector):
    guitar_vector, bass_vector = trim_start(guitar_vector[::-1], bass_vector[::-1])
    return guitar_vector[::-1], bass_vector[::-1]


def trim(bass_vector, guitar_vector):
    return trim_end(*trim_start(guitar_vector, bass_vector))


def find_next_silence(bass_vector, guitar_vector):
    for i, parts in enumerate(zip(bass_vector, guitar_vector)):
        found_guitar = False
        found_bass = False
        for j in range(i, i+universal_sample_rate):
            if found_guitar and found_bass:
                break
            if not guitar_vector == 'o'*12:
                found_guitar = True
            if not bass_vector == 'o'*12:
                found_bass = True
        if not found_guitar and not found_bass:
            return i


def split_silence(bass_vector, guitar_vector):
    while bass_vector:
        next_silence = find_next_silence(bass_vector, guitar_vector)
        if not next_silence:
            yield bass_vector, guitar_vector
            break
        yield bass_vector[:next_silence], guitar_vector[:next_silence]
        guitar_vector, bass_vector = trim(guitar_vector[next_silence:], bass_vector[next_silence:])


def allign_parts(guitar, bass):
    length = max([get_length(guitar), get_length(bass)])
    guitar_vector = to_vector(guitar, length)
    bass_vector = to_vector(bass, length)

    guitar_vector, bass_vector = trim(guitar_vector, bass_vector)
    #yield guitar_vector, bass_vector
    for parts in split_silence(bass_vector, guitar_vector):
        yield parts


def parse_gp_file(file_name):
    song = gp.parse(file_name)
    for guitar, bass in product(*get_guitar_bass(song)):
        guitar = get_notes(guitar)
        bass = get_notes(bass)
        for guitar_part, bass_part in allign_parts(guitar, bass):
            assert len(guitar_part) == len(bass_part)
            yield guitar_part, bass_part