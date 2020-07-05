
'''
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import os
import numpy as np
from keras import utils

data_path = 'static/asag_model/data/'
stu_answers = pd.read_csv(os.path.join(data_path, 'stu-answers.csv'), encoding='utf-8')
stu_answers = stu_answers.replace(np.nan, '', regex=True)


# preprocessing

# stop words
#f= open("/content/drive/My Drive/Data/ar_stopwords.txt", "r")
#ar_stopwords = f.read().split()

import nltk
nltk.download('stopwords')
# stop words
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
nltk.download('wordnet')

from nltk.stem.arlstem import ARLSTem
stemmmer = ARLSTem()

def remove_stowords(elements):
  corps = []
  for string in elements :
    #string = string.strip()
    string = string.split()
    string = [ stemmmer.stem(word) for word in string if not word in arb_stopwords ]
    string = ' '.join(string)
    corps.append(string)
  return corps


stu_answers['stu_answer'] = stu_answers['stu_answer'].apply(lambda x: " ".join(x.lower() for x in str(x).split() \
                                    if x not in arb_stopwords))
answers = stu_answers['stu_answer'].tolist()
scores = stu_answers['grade'].tolist()
scores = utils.to_categorical(scores)
corps = remove_stowords(answers)

# tokenization
from keras.preprocessing.text import Tokenizer,text_to_word_sequence , one_hot , text_to_word_sequence
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer.fit_on_texts(corps)
sequences = tokenizer.texts_to_sequences(corps)
max_sequence_length = max(len(s) for s in sequences)
sequences = pad_sequences(sequences,max_sequence_length)
word2idx = tokenizer.word_index
vocab_size = len(word2idx) + 1

from keras.models import load_model
model_path = 'static/asag_model/'
model = load_model(os.path.join(model_path, 'islamic_model.h5'))

def preprocces_input(input_ans):
  input_ans = remove_stowords(input_ans)
  input_ans = tokenizer.texts_to_sequences(input_ans)
  input_seq= pad_sequences(input_ans, maxlen=max_sequence_length)
  return input_seq

def predict(input_ans) :
  input_ans = [input_ans]
  input_ans = preprocces_input(input_ans)
  pred = model.predict_classes(input_ans)
  return pred[0]

'''

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import os
import numpy as np
from keras import utils

from keras.models import load_model


# read data
data_path = 'static/asag_model/data/'
all_answers = pd.read_csv(os.path.join(data_path, 'stu-answers.csv'), encoding='utf-8')
all_answers = all_answers.replace(np.nan, '', regex=True)

questions = pd.read_csv(os.path.join(data_path, 'questions.csv'), encoding='utf-8')
questions = questions.replace(np.nan, '', regex=True)

# preprocessing

# stop words
# f= open("/content/drive/My Drive/Data/ar_stopwords.txt", "r")
# ar_stopwords = f.read().split()

import nltk

nltk.download('stopwords')
# stop words
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
nltk.download('wordnet')

from nltk.stem.arlstem import ARLSTem

stemmmer = ARLSTem()

def remove_stowords(elements):
  corps = []
  for string in elements:
    # string = string.strip()
    string = string.split()
    string = [stemmmer.stem(word) for word in string if not word in arb_stopwords]
    string = ' '.join(string)
    corps.append(string)
  return corps

def predict(input_ans , prof_name , template_name):
  model_path = 'static/templates/'
  model_path = model_path + prof_name + '/' + template_name +'/models/'
  model_path = os.path.join(model_path, 'islamic_model.h5' )
  input_ans = [input_ans]
  input_ans = preprocces_input(input_ans)
  model = load_model(model_path)
  pred = model.predict_classes(input_ans)
  result =  pred[0]
  return result


def preprocces_input(input_ans):
  all_answers['stu_answer'] = all_answers['stu_answer'].apply(lambda x: " ".join(x.lower() for x in str(x).split() \
                                                                                 if x not in arb_stopwords))
  answers = all_answers['stu_answer'].tolist()
  corps = remove_stowords(answers)

  from keras.preprocessing.text import Tokenizer
  from tensorflow.keras.preprocessing.sequence import pad_sequences

  tokenizer = Tokenizer(filters=''''!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''''')
  tokenizer.fit_on_texts(corps)
  sequences = tokenizer.texts_to_sequences(corps)
  max_sequence_length = max(len(s) for s in sequences)


  input_ans = remove_stowords(input_ans)
  input_ans = tokenizer.texts_to_sequences(input_ans)
  input_seq = pad_sequences(input_ans, maxlen=max_sequence_length)
  return input_seq

