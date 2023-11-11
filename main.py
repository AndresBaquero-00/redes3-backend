import os
import pymongo
from flask import request, jsonify, Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient(os.getenv('MONGODB_HOST'))
db  = client['sensors_data']
col = db['data']

@app.route('/')
def home():
    return jsonify({'ok': True, 'status': 200, 'message': 'Hello World!'})

@app.route('/api/v2/save', methods=['POST'])
def save_data():
    data = request.get_json()
    res = col.insert_one(data)
    return jsonify({'ok': True, 'status': 200, 'message': str(res.inserted_id)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
