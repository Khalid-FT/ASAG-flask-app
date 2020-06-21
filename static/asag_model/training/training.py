# to download pretrained arabic word Emb model https://fasttext.cc/docs/en/pretrained-vectors.html
from gensim.models import KeyedVectors
fasttext_model = KeyedVectors.load_word2vec_format('wiki.ar.vec')

import pandas as pd
import os
import numpy as np
# read data
data_path = 'Data'
stu_answers= pd.read_csv(os.path.join(data_path, 'stu-answers.csv'), encoding='utf-8')
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
    string = string.strip()
    string = string.split()
    string = [ stemmmer.stem(word) for word in string if not word in arb_stopwords ]
    string = ' '.join(string)
    corps.append(string)
  return corps
answers = stu_answers['stu_answer'].tolist()
scores = stu_answers['grade'].tolist()
scores = utils.to_categorical(scores)
corps = remove_stowords(answers)



# tokenization
from keras.preprocessing.text import Tokenizer,text_to_word_sequence , one_hot , text_to_word_sequence
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(filters=''''!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''''' )
tokenizer.fit_on_texts(corps)
sequences = tokenizer.texts_to_sequences(corps)
max_sequence_length = max(len(s) for s in sequences)
sequences = pad_sequences(sequences,max_sequence_length)
word2idx = tokenizer.word_index
vocab_size = len(word2idx) + 1

# word embedding
from keras.layers import Embedding
import numpy as np
EMBEDDING_DIM = 300
num_words = len(word2idx) + 1
# prepare embedding matrix
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, idx in word2idx.items():
    if (word in fasttext_model) :
        embedding_matrix[idx] = fasttext_model.get_vector(word)
    else :
      #embedding_matrix[idx] = fasttext_model.get_vector("unk")
      print("  word not exist in voca ---> " + word)    


# load pre-trained word embeddings into an Embedding layer
# note that we set trainable = False so as to keep the embeddings fixed
embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=max_sequence_length,
                            trainable=False)



# train model
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
print('Build model...')
model = Sequential()
model.add(embedding_layer)
#model.add(Embedding(vocab_size,50))
model.add(LSTM(16, activation='relu'))
model.add(Dense(3, activation='softmax'))

# try using different optimizers and different optimizer configs
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Train...')
model.fit(sequences, scores,
          batch_size=1, epochs=100)                           
model.save('islamic_model.h5')



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
