
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional, Activation
from keras.callbacks import ModelCheckpoint
import numpy as np
from random import randint
import h5py

maxlen=40


def prepare_datasets(filename):
    text = open(filename, 'r', encoding='utf-8')

    words_train=[]
    words_test=[]

    for line in text:
        #remove bad symbols
        tmp=line.split('#')[1]
        tmp=tmp.replace("`", "")
        tmp=tmp.replace("\n","")

        #add missing accentures
        tmp=tmp.replace("ё", "ё'")

        #create test and train
        if randint(0,2)<2:
            words_train.extend(tmp.split(","))
        else:
            words_test.extend(tmp.split(","))

    #print(words_train[0:500])

    chars = sorted(list(set(''.join(words_train))))
    print('total chars:', len(chars))
    print(chars)
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    #print(len(char_indices))

    return words_train, words_test, char_indices, indices_char

def build_matrices(words):
    X = np.zeros((len(words), maxlen, len(char_indices) ), dtype=np.bool)
    y = np.zeros((len(words), maxlen), dtype=np.bool)
    for i, word in enumerate(words):

        try:
            acc_index=word.index("'")
            y[i,maxlen-len(word)+acc_index] = 1
        except:
            continue
        word2=word.replace("'","")
        for index, letter in enumerate(word2):
            pos=maxlen-len(word2)+index
            X[i, pos, char_indices[letter]]=1

    return X, y

words_train, words_test, char_indices, indices_char = prepare_datasets ('Accented_All_Forms.txt')
X_train, y_train = build_matrices(words_train)
X_test, y_test = build_matrices(words_test)

print('Build model...')
model = Sequential()
#model.add(Dense(len(words3), len(chars), input_length=maxlen))
model.add(Bidirectional(LSTM(64), input_shape=(maxlen, len(char_indices))))
model.add(Dropout(0.2))
model.add(Dense(maxlen))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

filepath="weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3, batch_size=64, callbacks=callbacks_list)

json_string = model.to_json()
with open("model.json", "w") as text_file:
    text_file.write(json_string)

#model.save('weights-improvement-02-0.88.h5')


