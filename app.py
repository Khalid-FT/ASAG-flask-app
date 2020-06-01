import warnings
warnings.filterwarnings('ignore')


from flask import Flask,request,jsonify
import methodes
from static.asag_model.full_model import predict
import json
import os

app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

'''
   request : POST 
   Format : { "step": "tokenization" , "body":"khalid fatah"} steps = [tokenization, diacritization, lemma, stopwords]
   response : { "body": [ "khalid", "fatah" ], "step": "tokenization" }
'''
@app.route('/process', methods=['POST'])
def process():
  elem = request.json
  step = elem['step']
  body = elem['body']
  step, body = methodes.procces(step, body)
  elem = {'step': step, 'body': body}
  return jsonify(elem)

templates_dir = 'static/templates/'
'''
   request : POST 
   format : [ {"prof_name": "prof1" , "template_name": "template1"},{"question": "question1" ,"answer": "refanswer1" }]
   response : json template
'''
@app.route('/addtemplate' , methods=['POST'])
def addTemplate():
    req = request.json
    template = []
    prof_name = req[0]['prof_name']
    template_name = req[0]['template_name']
    template.append({'prof_name': prof_name , 'template_name': template_name})
    for elem in req:
      if 'prof_name' in elem :
        continue
      else :
        question = elem['question']
        ref_answer = elem['answer']
        response = {'question': question , 'answer': ref_answer}
        template.append(response)

    dir_prof = os.path.join(templates_dir,prof_name)
    if not os.path.exists(dir_prof):
       os.mkdir(dir_prof)
    json_path = os.path.join(dir_prof, template_name + '.json')
    with open(json_path, 'w' , encoding='utf8') as json_file:
        json.dump(template, json_file)
    return jsonify({'msg':'template added!'})

'''
   request : GET 
   params : temp & prof
   response : json template
'''
@app.route('/asag' , methods=['GET'])
def template():
  template_name = request.args.get('temp')
  prof_name = request.args.get('prof')
  dir_prof = os.path.join(templates_dir, str(prof_name))
  json_file = os.path.join(dir_prof, str(template_name)+'.json')
  template = []
  if os.path.exists(json_file):
      with open(json_file, 'r', encoding='utf-8') as f:
          template = json.load(f)
  return jsonify(template)

'''
   request : POST 
   Format : [ { "question": "who am i ?" , "answer":"khalid fatah"}, { "question": "city ?" , "answer":"Tanger"}, {} , {}  ]
   response : [ { "question": "who am i ?" , "answer":"khalid fatah" , "score": "5" }, {} , {} , {}  ]
'''
@app.route('/asag', methods=['POST'])
def asag():
  asag_requset = request.json
  asag_response = []
  for elem in asag_requset :
    question =  elem['question']
    answer = elem['answer']
    score = str(0)
    if (methodes.validAnswer(answer)) == True : score = str(predict(answer))
    response = { 'question': question , 'answer': answer , 'score': score }
    asag_response.append(response)
  return jsonify(asag_response)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,threaded=False)


