import warnings
warnings.filterwarnings('ignore')

import os
import  json
from flask import Flask,request,jsonify
import methodes
from static.asag_model.model import predict

app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

templates_dir = 'static//templates'
@app.route('/asag' , methods=['GET'])
def template():
  temp = request.args.get('q')
  with open(os.path.join(templates_dir, str(temp)+'.json') , 'r' , encoding='utf-8') as f:
    template = json.load(f)
  return jsonify(template)

@app.route('/process', methods=['POST'])
def process():
  elem = request.json
  step = elem['step']
  body = elem['body']
  step, body = methodes.procces(step, body)
  elem = {'step': step, 'body': body}
  return jsonify(elem)

@app.route('/asag', methods=['POST'])
def asag():
  asag_requset = request.json
  asag_response = []
  for elem in asag_requset :
    question =  elem['question']
    answer = elem['answer']
    score = str(predict(answer))
    response = { 'question': question , 'answer': answer , 'score': score }
    asag_response.append(response)
  return jsonify(asag_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,threaded=False)


