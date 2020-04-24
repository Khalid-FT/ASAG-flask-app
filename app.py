import warnings
warnings.filterwarnings('ignore')

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

@app.route('/')
def home():
  return 'hello backend! this flask'

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
  element = request.json
  for (i,elem) in enumerate(element) :
    element[i]['score'] = str(predict(elem['body']))
  return jsonify(element)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,threaded=False)


