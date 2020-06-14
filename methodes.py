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

import re
def reg_score(answer,keywords):
    counter = 0
    reg_score = '0/0'
    regScore = 0
    pattern = '('
    for keyword in keywords:
        if len(keyword) != 0:
            counter += 1
    if counter == 1:
        keyws = keywords[0][0].split(';')
        for i, k in enumerate(keyws):
            if i == len(keyws) - 1:
                pattern = pattern + k + ')'
                break
            pattern = pattern + k + '|'
        results = re.findall(pattern, answer)
        if len(results) != 0: reg_score = '1/1'
        else  : reg_score = '0/1'
    elif counter == 2:
        for i in range(0, 2):
            keyws = keywords[i][0].split(';')
            if i == 0:
                for j, k in enumerate(keyws):
                    if j == len(keyws) - 1:
                        pattern = pattern + k + ')'
                        break
                    pattern = pattern + k + '|'
                results = re.findall(pattern, answer)
                if len(results) != 0: regScore = regScore + 1
                pattern = '('
            if i == 1:
                for j, k in enumerate(keyws):
                    if j == len(keyws) - 1:
                        pattern = pattern + k + ')'
                        break
                    pattern = pattern + k + '|'
                results = re.findall(pattern, answer)
                if len(results) != 0: regScore = regScore + 1
                pattern = '('
        reg_score = str(regScore) + '/2'
    elif counter == 3:
        for i in range(0, 3):
            keyws = keywords[i][0].split(';')

            if i == 0:
                for j, k in enumerate(keyws):
                    if j == len(keyws) - 1:
                        pattern = pattern + k + ')'
                        break
                    pattern = pattern + k + '|'
                results = re.findall(pattern, answer)
                if len(results) != 0: regScore = regScore + 1
                pattern = '('
            if i == 1:
                for j, k in enumerate(keyws):
                    if j == len(keyws) - 1:
                        pattern = pattern + k + ')'
                        break
                    pattern = pattern + k + '|'
                results = re.findall(pattern, answer)
                if len(results) != 0: regScore = regScore + 1
                pattern = '('
            if i == 2:
                for j, k in enumerate(keyws):
                    if j == len(keyws) - 1:
                        pattern = pattern + k + ')'
                        break
                    pattern = pattern + k + '|'
                results = re.findall(pattern, answer)
                if len(results) != 0: regScore = regScore + 1
                pattern = '('
        reg_score = str(regScore) + '/3'
    elif counter == 4:
        for i in range(0, 4):
            keyws = keywords[i][0].split(';')
            if i == 0:
                for j, k in enumerate(keyws):
                    if j == len(keyws) - 1:
                        pattern = pattern + k + ')'
                        break
                    pattern = pattern + k + '|'
                results = re.findall(pattern, answer)
                if len(results) != 0: regScore = regScore + 1
                pattern = '('
            if i == 1:
                for j, k in enumerate(keyws):
                    if j == len(keyws) - 1:
                        pattern = pattern + k + ')'
                        break
                    pattern = pattern + k + '|'
                results = re.findall(pattern, answer)
                if len(results) != 0: regScore = regScore + 1
                pattern = '('
            if i == 2:
                for j, k in enumerate(keyws):
                    if j == len(keyws) - 1:
                        pattern = pattern + k + ')'
                        break
                    pattern = pattern + k + '|'
                results = re.findall(pattern, answer)
                if len(results) != 0: regScore = regScore + 1
                pattern = '('
            if i == 3:
                for j, k in enumerate(keyws):
                    if j == len(keyws) - 1:
                        pattern = pattern + k + ')'
                        break
                    pattern = pattern + k + '|'
                results = re.findall(pattern, answer)
                if len(results) != 0: regScore = regScore + 1
                pattern = '('
        reg_score = str(regScore) + '/4'
    return  reg_score
