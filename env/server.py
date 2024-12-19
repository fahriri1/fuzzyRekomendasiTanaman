from flask import Flask, render_template, request
import requests
from fuzzyModel import calcFuzzy

app = Flask(__name__)

@app.route('/')
def index():
    print("testing")
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)