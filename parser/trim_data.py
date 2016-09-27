import os

path = 'data/'


def trim_start(lines):
    for i, line in enumerate(lines):
        if not 'o'*12 in line:
            return lines[i:]


def trim_end(lines):
    for i in xrange(len(lines)-1, -1, -1):
        if not 'o'*12 in lines[i]:
            return lines[:i+1]


for file in os.listdir(path):
    if file.startswith('.'):
        continue
    lines = open(path+file).read().split('\n')
    lines = trim_start(lines)
    lines = trim_end(lines)
    if lines:
        with open(path+file, 'w') as fp:
            for line in lines:
                fp.write(line+'\n')
    else:
        print file
        os.remove(path+file)