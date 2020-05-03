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
  corps = []
  string = text.strip()
  string = string.split()
  string = [word for word in string if not word in arb_stopwords]
  string = ' '.join(string)
  corps.append(string)
  return corps

def diacritize(text):
  return diacritization(text)

def tokenization(text):
  return text.split()

def stemmer(text):
  return stem.stem(text)

def pos(text):
  text = TextBlob(text)
  return text.tags

def spellCheck(text):
  text = TextBlob(text)
  return str(text.correct())

def procces(step,body) :
  if(step == 'tokenization') : body = tokenization(body)
  elif (step == 'spelling') : body = spellCheck(body)
  elif (step == 'diacritization'): body = diacritize(body)
  elif ( step == 'lemma' ) : body = stemmer(body)
  elif (step == 'stopwords'): body = removeStopWords(body);
  elif (step == 'post'): body = pos(body);
  return step , body

