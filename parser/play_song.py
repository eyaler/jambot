from mido import Message
import time

class song_player():
    def __init__(self, tempo):
        self.tempo = tempo/1000.
        self.state = [False]*12
        self.key = 48

    def play_song(self, lines):
        for line in lines:
            time.sleep(self.tempo)
            self.play_note(line)

    def play_note(self, line):
        for i, c in enumerate(line):
            if state[i]:
                if not c == 'i':
                    Message('note_off', note=self.key + i)
                    state[i] = False

            if c == 'b':
                state[i] = True
                Message('note_on', note=self.key+i)

