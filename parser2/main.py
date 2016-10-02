from gp_file_yielder import yield_gp_files
from parse_gp_file import parse_gp_file
from config import *

if __name__ == '__main__':
    for file_name in yield_gp_files(gp_folder):
        for guitar_part, bass_part in parse_gp_file(file_name):
            pass