from flask import Flask, render_template, request, jsonify
import requests
from fuzzyModel import calcFuzzy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    respons = request.json
    pisang_, kentang_, jagung_ =  calcFuzzy(int(respons['temp']), int(respons['rain']), int(respons['humid']))
    data = {
        'pisang' : pisang_,
        'kentang' : kentang_,
        'jagung' : jagung_
    }
    print(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)