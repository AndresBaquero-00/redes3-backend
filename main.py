import os
from flask import request, jsonify, Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'ok': True, 'status': 200, 'message': 'Hello World!'})

@app.route('/api/v2/save')
def save_data():
    print(request.method)
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify({'ok': True, 'status': 200, 'message': 'Hello World!'})
    
    return jsonify({'ok': False, 'status': 400})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
