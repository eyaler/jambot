# use author folders in parser
# and load model
# truncated backprop in time, unroll, consume less
# do i need separate train/test models?
# masking/end of message symbol
# most of the output are zero
# add end-end to time descritization (similar to start-start); do it globally instead of locally?
# attention
# time windows
# context and consistency
# train like test papers
# diversity objective
# make sure we get difference from corpus
# fix midi latency
# find a better measure than accuracy (balanced acc/balanced recall)
# tempo?
# calibrate tempo for demo, listen to overfitted music
# deal with illegal i after o in training: a) do nothing b) count i as correct c) ignore the i option and compare b and o probabilities
# compare transposed scale vs not
# due to multiple versions validate may have same songs as train
# save stats, plot history, how to deal with chunked training?
# global config params
# learn velocity
# if only one file take its size
# if no validation use train loss for saving
# tal suggest: predict 1/36 global state instead of per note , or ignore o's (how to do unbalanced log loss)
# change instruments for track
# s0 vs st vs step
# how does alignment work for input (in real life you are not exactly on the beat - allow noise for this)
# play in loop longer than song length
# compare overfit on one file
# weightd logloss? give more weight to b?
# where to put the sleep?
# make sure we do not play for zero input?
# why did i have(len(X)==0) problems?


from keras.preprocessing.sequence import pad_sequences
import keras.backend as K
import os
import numpy as np
from utils import load_song
from net import get_train_model, get_train_model1
from time import time

limit = None
valid_frac = 0.1
epochs = 1000
chunk_size = 2000
batch_size = 32
mode = 1
data_folder = 'd:/data/jambot'
hard_max_len = 6000
load_model = False

filenames = os.listdir(data_folder)[:limit]
np.random.seed(42)
np.random.shuffle(filenames)
f_valid= filenames[:int(len(filenames)*valid_frac)]
f_train = filenames[int(len(filenames)*valid_frac):]
chunks = 1
if chunk_size is not None:
    chunks = max(round(len(filenames)/chunk_size), 1)

lens = []
bads = 0
def load_chunk(current_filenames):
    global lens, bads
    X = []
    y = []
    for filename in current_filenames:
        try:
            rows0, rows1 = load_song(data_folder+'/' + filename)
        except Exception as e:
            if lens is not None and len(lens) < len(filenames) - bads:
                print('bad: %s : %s' % (e, filename))
                bads += 1
            continue
        X.append(rows0)
        y.append(rows1)
        if lens is not None:
            lens.append(len(rows0))
    if lens is not None and len(lens)==len(filenames)-bads:
        print('good=%d bad=%d / files=%d' % (len(lens), bads, len(filenames)))
        assert len(lens)>0
        print('min=%d, max=%d, mean=%.1f, std=%.1f, meadian=%.1f 75%%==%.1f 90%%==%.1f 95%%==%.1f' % (
            min(lens), max(lens), np.mean(lens), np.std(lens), np.median(lens), np.percentile(lens, 75),
            np.percentile(lens, 90), np.percentile(lens, 95)))
        lens = None


    if mode == 1:
        y_helper = np.zeros_like(y)
        y_helper[:, 1:] = y[:, :-1]
        X = [X, y_helper]
    return X, y

def bacc(y_true, y_pred): #not finished
    return K.mean(K.equal(K.argmax(y_true, axis=-1),
                   K.argmax(y_pred, axis=-1)))


y_valid = []
X_valid, y_valid = load_chunk(f_valid)

if mode==0:
    model = get_train_model(hard_max_len)
else:
    model = get_train_model1(hard_max_len)
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy', bacc])

best_loss = None
if load_model and os.path.exists('models/model'+str(mode)+'.h5'):
    model.load_weights('models/model'+str(mode)+'.h5')
    if len(y_valid) > 0:
        val_loss = model.evaluate(X_valid, y_valid, batch_size=batch_size)
        print ('loaded val_loss=%.4f val_acc=%.4f val_bacc=%.4f'%(val_loss[0],val_loss[1],val_loss[2]))
        best_loss = val_loss[0]

start = time()
for epoch in range(epochs):
    print ('epoch: %d/%d'%(epoch+1,epochs))
    epoch_start = time()
    for i in range(chunks):
        print('chunk: %d/%d' % (i+1,chunks))
        chunk_start = time()
        if epoch==0 or chunks>1:
            y_train = []
            X_train, y_train = load_chunk(f_train[int(i*len(f_train)/chunks):int((i+1)*len(f_train)/chunks)])
        if len(y_train)>0:
            model.fit(X_train, y_train, nb_epoch=1, batch_size=batch_size)
        if chunks>1:
            del X_train, y_train
        print('chunk took %.1f min' % ((time() - chunk_start)/60))
    print ('epoch took %.1f min / total %.1f min'%((time()-epoch_start)/60, (time()-start)/60))
    if len(y_valid)>0:
        val_loss = model.evaluate(X_valid, y_valid, batch_size=batch_size)
        print ('val_loss=%.4f val_acc=%.4f val_bacc=%.4f'%(val_loss[0],val_loss[1],val_loss[2]))
        if best_loss is None or val_loss[0]<best_loss:
            best_loss = val_loss[0]
            model.save_weights('models/model'+str(mode)+'.h5')
if len(y_valid)==0:
    model.save_weights('models/model'+str(mode)+'.h5')
print('training finished %.1f min' % ((time() - start)/60))