import warnings
warnings.filterwarnings('ignore')


import os
import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import numpy as np


max_sentence = 315

def load_binary(file, folder):
    location  = os.path.join(folder, (file+'.pickle') )
    with open(location, 'rb') as ff:
        data = pickle.load(ff)
    return data

def prepare_input(input_sent):
    assert input_sent != None and len(input_sent) < max_sentence, \
        "max length for input_sent should be {} characters, you can split the sentence into multiple sentecens and call the function".format(
            max_sentence)

    input_sent = [input_sent]

    return __preprocess(input_sent)

def __preprocess(input_sent):

    input_vocab_to_int = dictionary["input_vocab_to_int"]

    input_letters_ids  = [[input_vocab_to_int.get(ch, input_vocab_to_int['<UNK>']) for ch in sent] for sent in input_sent]

    input_letters_ids  = __pad_size(input_letters_ids, max_sentence)

    return input_letters_ids

def __pad_size(x, length=None):
    return pad_sequences(x, maxlen=length, padding='post')

def logits_to_text(logits):
    text = []
    for prediction in np.argmax(logits, 1):
        if dictionary['output_int_to_vocab'][prediction] == '<PAD>':
            continue
        text.append(dictionary['output_int_to_vocab'][prediction])
    return text

def combine_text_with_harakat(input_sent, output_sent):
    # fix combine differences
    input_length = len(input_sent)
    output_length = len(output_sent)  #
    for index in range(0, (input_length - output_length)):
        output_sent.append("")

    # combine with text
    text = ""
    for character, haraka in zip(input_sent, output_sent):
        if haraka == '<UNK>' or haraka == 'ـ':
            haraka = ''
        text += character + "" + haraka
    return text

def get_final_text(input_sent, output_sent):
    return combine_text_with_harakat(input_sent, output_sent)

dictionary_folder = 'static/Shakkala_model/dictionary'
input_vocab_to_int  = load_binary('input_vocab_to_int',dictionary_folder)
output_int_to_vocab = load_binary('output_int_to_vocab',dictionary_folder)
dictionary = { "input_vocab_to_int":input_vocab_to_int,
                "output_int_to_vocab":output_int_to_vocab }


def diacritization(input_text) :
    # prepare input
    input_int = prepare_input(input_text)
    model = load_model('static/Shakkala_model/second_model6.h5')
    logits = model.predict(input_int)[0]
    predicted_harakat = logits_to_text(logits)
    final_output = get_final_text(input_text, predicted_harakat)
    return final_output


