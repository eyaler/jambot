from gp_file_yielder import yield_gp_files
from parse_gp_file import parse_gp_file
from config import *

if __name__ == '__main__':
    for file_name in yield_gp_files(gp_folder):
        for i, (guitar_part, bass_part) in enumerate(parse_gp_file(file_name)):
            file_name = file_name.split('/')[-1].split('.')[0]+str(i)
            with open(out_folder+file_name, 'w') as fp:
                for line in zip(bass_part, guitar_part):
                    fp.write(','.join(line)+'\n')