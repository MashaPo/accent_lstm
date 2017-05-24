
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional, Activation
from keras.callbacks import ModelCheckpoint
import numpy as np
from random import randint
import os
import re
import h5py

MAXLEN=40
VOWELS = 'аеиоуэюяыё'
REG = '[{}].*[{}]'.format(VOWELS, VOWELS)

def add_endings(wordlist):
    pluswords = []
    for i,word in enumerate(wordlist):
        if not bool(re.search(REG, word)):
            continue
        elif i == 0 or wordlist[i-1] == '_':
            pluswords.append('_' + word)
        else:
            context = wordlist[i-1].replace("'", "")
            if len(context)<3:
                ending = context
            else:
                ending = context[-3:]
            plusword = ending + '_' + word
            pluswords.append(plusword)
    return pluswords

def prepare_datasets(directory):
    words_train = []
    words_test = []
    dirs = os.walk(directory)
    for dir in dirs:  # ('nkrja\\reading\\zoschenko', [], ['zo-rasp.xml'])
        print('on directory {} '.format(dir))
        files = dir[2]
        for file in files:
            filename = dir[0] + '/' + file
            print('opening {}...'.format(filename))
            file = open(filename, 'r', encoding='utf-8')
            text = file.read()
            text = text.replace("ё", "ё'")
            text = text.replace("c", "с") # latinic to cyrillic
            regex1 = "[…:,.?!\n]"
            text = re.sub(regex1, " _ ", text).lower() #mark beginning of clause
            regex2 = "[^а-яё'_ -]" # get rid of "#%&""()*-[0-9][a-z];=>@[\\]^_{|}\xa0'
            text = re.sub(regex2, "", text)

            words = text.split(' ')
            #print(words[:50])
            pluswords = add_endings(words)
            for plusword in pluswords:
                #create test and train
                if randint(0,2)<2:
                    words_train.append(plusword)
                else:
                    words_test.append(plusword)

    print('trainset total {}'.format(len(words_train)))
    print(words_train[:50])
    print('testset total {}'.format(len(words_test)))
    print(words_test[:50])

    chars = sorted(list(set(''.join(words_train))))
    print('total chars:', len(chars))
    print(chars)
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

        #print(len(char_indices))

    return words_train, words_test, char_indices, indices_char

def build_matrices(words):
    X = np.zeros((len(words), MAXLEN, len(char_indices) ), dtype=np.bool)
    y = np.zeros((len(words), MAXLEN), dtype=np.bool)
    for i, word in enumerate(words):
        if word.count("'") == 1:
            acc_index=word.index("'")
            y[i,MAXLEN-len(word)+acc_index] = 1
        else:
            continue
        word2=word.replace("'","")
        for index, letter in enumerate(word2):
            pos=MAXLEN-len(word2)+index
            X[i, pos, char_indices[letter]]=1
    return X, y

DIR = 'C:/hse_compling/stress_corpora/nkrja/txt_acc_nkrja'
#DIR = 'C:/hse_compling/stress_corpora/nkrja/test'
words_train, words_test, char_indices, indices_char = prepare_datasets(DIR)
X_train, y_train = build_matrices(words_train)
X_test, y_test = build_matrices(words_test)

print('Build model...')
model = Sequential()
#model.add(Dense(len(words3), len(chars), input_length=MAXLEN))
model.add(Bidirectional(LSTM(64), input_shape=(MAXLEN, len(char_indices))))
model.add(Dropout(0.2))
model.add(Dense(MAXLEN))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

filepath="weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3, batch_size=64, callbacks=callbacks_list)

json_string = model.to_json()
with open("model.json", "w") as text_file:
    text_file.write(json_string)



