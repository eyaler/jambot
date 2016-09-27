import guitarpro as gp
import os



def get_dirs(path):
    for file_or_dir in os.listdir(path):
        if os.path.isdir(path+file_or_dir):
            yield path+file_or_dir+'/'


def got_guitar_bass(song):
    guitar = False
    bass = False
    for track in song.tracks:
        if 'guitar' in track.name.lower():
            guitar = True
        if 'bass' in track.name.lower():
            bass = True
    return guitar and bass

gp_folder = '/Users/talbaumel/Dropbox/Guitar Pro Tabs - 55000/'

count = 0
for letter in get_dirs(gp_folder):
    for band in get_dirs(letter):
        for file_name in os.listdir(band):

            if file_name.startswith('.'):
                continue
            file_name = band+file_name

            try:
                guitar_pro_file = gp.parse(file_name)
                if got_guitar_bass(guitar_pro_file):
                    count += 1
            except:
                os.remove(file_name)
                print file_name

print count
            #for track in guitar_pro_file.tracks:
            #    print track.name

            #    for measure in track.measures:

            #        for voice in measure.voices:
            #            for beat in voice.beats:
            #                for note in beat.notes:
            #                    print note.string, note.value



