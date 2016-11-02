import os


def get_dirs(path):
    for file_or_dir in os.listdir(path):
        if os.path.isdir(path+file_or_dir):
            yield path+file_or_dir+'/'



def yield_gp_files(gp_folder):
    for letter in get_dirs(gp_folder):
        for band in get_dirs(letter):
            for file_name in os.listdir(band):
                if file_name.startswith('.'):
                    continue
                file_name = band + file_name
                yield file_name, band.split('/')[-2]