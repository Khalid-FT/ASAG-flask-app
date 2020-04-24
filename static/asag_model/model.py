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

# preprocessing
import nltk

nltk.download('stopwords')
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
nltk.download('wordnet')


def preprocess_data(elements):
  corps = []
  for string in elements:
    string = string.strip()
    string = string.split()
    string = [word for word in string if not word in arb_stopwords]
    string = ' '.join(string)
    corps.append(string)
  return corps


'''
type 1 : "Define the scientific term",
type 2 : "Explain",
type 3 : "What are the consequences of"
type4 : "Why".
'''

# question
id_question = '1_1'
question = questions['question'].loc[questions['id_question'] == id_question]
print('question: ', question.to_list()[0])

from keras import utils

# training answers and score
train = stu_answers['stu_answer'].loc[stu_answers['idx_quest_ref'] == id_question]
train_scores = stu_answers['rater1'].loc[stu_answers['idx_quest_ref'] == id_question]
train_scores = utils.to_categorical(train_scores, 6)

# tokenization
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

corps = preprocess_data(train)

tokenizer = Tokenizer(filters=''''!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''''')
tokenizer.fit_on_texts(corps)
sequences = tokenizer.texts_to_sequences(corps)
max_sequence_length = max(len(s) for s in sequences)
sequences = pad_sequences(sequences, max_sequence_length)
word2idx = tokenizer.word_index
vocab_size = len(word2idx) + 1

print(sequences.shape)

from keras.models import load_model

model = load_model('static/asag_model/model.h5')

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

