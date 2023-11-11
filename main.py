import json
import os
import pymongo
from Crypto.Cipher import AES
from Crypto.Util import Padding
from flask import request, jsonify, Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient(os.getenv('MONGODB_HOST'))
db  = client['sensors_data']
col = db['data']

cipher = AES.new(bytes.fromhex(os.getenv('CRYPTO_KEY')), AES.MODE_ECB)

@app.route('/')
def home():
    return jsonify({'ok': True, 'status': 200, 'message': 'Hello World!'})

@app.route('/api/v2/save', methods=['POST'])
def save_data():
    data = request.get_json()
    res = col.insert_one(data)
    return jsonify({'ok': True, 'status': 200, 'message': str(res.inserted_id)})

@app.route('/api/v2/save-secure', methods=['POST'])
def save_data_secure():
    data = request.get_data().decode()
    raw = Padding.unpad(cipher.decrypt(bytes.fromhex(data)), 16).decode()
    res = col.insert_one(json.loads(raw))
    return jsonify({'ok': True, 'status': 200, 'message': str(res.inserted_id)})

@app.route('/api/v2/list', methods=['GET'])
def list_data():
    data = col.find().sort({'datetime': -1}).limit(10)
    for d in list(data):
        print(d)
    return jsonify({'ok': True, 'status': 200, 'message': 'Operación realizada exitosamente.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
