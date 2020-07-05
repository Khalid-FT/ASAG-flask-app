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

def predict(input_ans, question , prof_name , template_name):
  id_q = questions['id_question'].loc[questions['question'] == question].tolist()[0]
  model_path = 'static/templates/'
  model_path = model_path + prof_name + '/' + template_name +'/models/'
  model_path = os.path.join(model_path, str(id_q) +'.h5' )
  input_ans = [input_ans]
  input_ans = preprocces_input(input_ans, id_q)
  model = load_model(model_path)
  pred = model.predict_classes(input_ans)
  result =  pred[0]
  return result


def preprocces_input(input_ans, id_q):
  stu_answers = all_answers.loc[all_answers['id_question'] == id_q]
  stu_answers['stu_answer'] = stu_answers['stu_answer'].apply(lambda x: " ".join(x.lower() for x in str(x).split() \
                                                                                 if x not in arb_stopwords))
  answers = stu_answers['stu_answer'].tolist()
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

