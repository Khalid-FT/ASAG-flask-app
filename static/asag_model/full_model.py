import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import os

'''
type 1 : "Define the scientific term",
type 2 : "Explain",
type 3 : "What are the consequences of"
type4 : "Why".
'''

data_path = 'static/asag_model/data/'
questions = pd.read_csv(os.path.join(data_path, 'questions.csv'), encoding='utf-8')
ref_answers = pd.read_csv(os.path.join(data_path, 'ref_answers.csv'), encoding='utf-8')
stu_answers = pd.read_csv(os.path.join(data_path, 'stu_answer.csv'), encoding='utf-8')

from keras import utils

# training data
X_train = stu_answers['stu_answer']
y_train = stu_answers['rater1']
y_train = utils.to_categorical(y_train,6)

# preprocessing
import nltk
nltk.download('stopwords')
# stop words
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
nltk.download('wordnet')
from nltk.corpus import stopwords
import re

# stemming
#!pip install tashaphyne
#from tashaphyne.stemming import ArabicLightStemmer
from nltk.stem.arlstem import ARLSTem
from nltk.stem.isri import ISRIStemmer
stem1 = ARLSTem()
stem2= ISRIStemmer()

def preprocess_data(elements):
  corps = []
  for string in elements :
    string = string.strip()
    string = string.split()
    string = [stem1.stem(word) for word in string if not word in arb_stopwords  ]
    string = ' '.join(string)
    corps.append(string)
  return corps

# tokenization
from keras.preprocessing.text import Tokenizer,text_to_word_sequence , one_hot , text_to_word_sequence
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

corps = preprocess_data(X_train)

tokenizer = Tokenizer(filters=''''!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''''' )
tokenizer.fit_on_texts(corps)
sequences = tokenizer.texts_to_sequences(corps)
max_sequence_length = max(len(s) for s in sequences)
sequences = pad_sequences(sequences,max_sequence_length)
word2idx = tokenizer.word_index
vocab_size = len(word2idx) + 1

print(sequences.shape)

from keras.models import load_model
model = load_model('static/asag_model/biology_model.h5')

def preprocces_input(input_ans):
  input_ans = preprocess_data(input_ans)
  input_ans = tokenizer.texts_to_sequences(input_ans)
  input_seq = pad_sequences(input_ans, maxlen=max_sequence_length)
  return input_seq

def predict(input_ans) :
  input_ans = [input_ans]
  input_ans = preprocces_input(input_ans)
  pred = model.predict_classes(input_ans)
  return pred[0]


