from utils import load_song, index2bio, song_player, one_hot, get_bio
from net import get_test_model, get_test_model1
import numpy as np
import time

test_filename = None
#test_filename = 'd:/data/jambot/Ramones (The) - Blitzkrieg Bop (4).gp333532'

temp = 1.0
mode = 1
octave_len = 12
states = 3
tempo = 127
volume_bass = 127
volume_lead = 104
pitch_offset_bass=0
pitch_offset_lead=12

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

if mode==0:
    model = get_test_model()
else:
    model = get_test_model1()
model.load_weights('model'+str(mode)+'.h5')
player = song_player(tempo=tempo)

if test_filename is not None:
    song, _ = load_song(test_filename)
    s2 = song.shape[1]
    s3 = song.shape[2]
else:
    song = get_bio(tempo=0)
    s2 = octave_len
    s3 = states
x = np.zeros([1, 1, s2, s3])
prev_y = np.zeros([1, 1, s2, s3])

x1 = x
if mode == 1:
    x1 = [x, prev_y] #first call to predict takes longer time
model.predict(x1)

started = False
print('ready')
for step in song:
    st = step
    if test_filename is None:
        if st!='o'*len(st):
            started=True
        st = one_hot(st)
        if not started:
            continue
    x[0, 0] = st
    x1 = x
    if mode==1:
        x1 = [x, prev_y]
    start_time = round(time.time() * 1000)
    y = model.predict(x1)
    total_time = start_time - round(time.time() * 1000)
    s = index2bio([sample(i, temp) for i in y[0]])
    prev_y[0, 0] = one_hot(s)
    time.sleep((tempo- total_time)/1000. )
    player.play_notes(s, volume=volume_lead, pitch_offset=pitch_offset_lead, track=1)
    s0 = index2bio([sample(i, temp) for i in st])
    player.play_notes(s0, volume=volume_bass, pitch_offset=pitch_offset_bass, track=0, sleep=False)
    print(s0,s)
