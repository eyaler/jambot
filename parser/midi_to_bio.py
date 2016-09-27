import mido
import time
from queue import Queue
from threading import Thread


mido.set_backend('mido.backends.rtmidi')


def listener(q):
    in_portname = None
    with mido.open_input(in_portname) as in_port:
        for message in in_port:
            q.put(message)


def get_bio(tempo):
    tempo = tempo/1000.
    q = Queue()
    t1 = Thread(target=listener, args=(q,))
    t1.start()

    start_note = 48
    state = ['o'] * 12
    while True:

        time.sleep(tempo)
        for i, c in enumerate(state):
            if c == 'b':
                state[i] = 'i'

        while not q.empty():
            message = q.get()

            type = message.type == 'note_on'
            note = (message.note-start_note)%12
            if type:
                state[note] = 'b'
            else:
                state[note] = 'o'
        yield ''.join(state)


if __name__ == '__main__':
    for state in get_bio(tempo = 1000):
        print state