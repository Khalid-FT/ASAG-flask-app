import warnings
warnings.filterwarnings('ignore')

import nltk
nltk.download('stopwords')
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
nltk.download('wordnet')
from textblob import TextBlob
from nltk.stem.arlstem import ARLSTem
stem = ARLSTem()
from static.Shakkala_model.diacritization import diacritization
def removeStopWords(text):
  string = text.strip()
  string = string.split()
  string = [word for word in string if not word in arb_stopwords]
  string = ' '.join(string)
  return string

def diacritize(text):
  return diacritization(text)

def tokenization(text):
  return text.split()

def stemmer(text):
  return stem.stem(text)

def procces(step,body) :
  if(step == 'tokenization') : body = tokenization(body)
  elif (step == 'diacritization'): body = diacritize(body)
  elif ( step == 'lemma' ) : body = stemmer(body)
  elif (step == 'stopwords'): body = removeStopWords(body);
  return step , body

from googletrans import Translator
translator = Translator()
def validAnswer(input_sen) :
  if len(input_sen) <= 0 or translator.detect(input_sen).lang != 'ar' :
    return False
  else :
    return True
