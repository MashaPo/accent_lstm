from keras.models import model_from_json
import numpy as np

def predict(model, word, maxlen, char_indices):
    x = np.zeros((1, maxlen, len(char_indices)), dtype=np.bool)
    print(word)
    for index, letter in enumerate(word):
        pos = maxlen - len(word.replace("'", "")) + index
        x[0, pos, char_indices[letter]] = 1
    print(x)
    preds = model.predict(x, verbose=0)[0]
    print(preds)
    preds = preds.tolist()
    max_value = max(preds)
    index = preds.index(max_value)
    index = len(word) - maxlen + index
    print(preds)
    print('max_value in preds is %s with index %s' % (max_value, index))
    if index > len(word)-1:
        print('no %s-th letter in %s' % (index+1,word))
    else:
        acc_word = word[:index+1]+'\''+ word[index+1:]
        return(acc_word)


def main():
    maxlen = 40
    chars = ["'", '-', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
             'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё']
    char_indices = dict((c, i) for i, c in enumerate(chars))
    with open("model.json", 'r') as content_file:
        json_string = content_file.read()
    model = model_from_json(json_string)
    model.load_weights('weights-improvement-02-0.88.hdf5')

    while True:
        word = input("Russian word to accentuate: ")
        word = word.strip(' ').lower()
        if len(set(word) - set(chars)) == 0:
            acc_word = predict(model, word, maxlen, char_indices)
            print(acc_word)
        else:
            print ('only russian allowed')
            continue

if __name__ == "__main__":
    main()