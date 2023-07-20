#!/usr/bin/python
from flask import Flask
app = Flask(__name__)


@app.route('/')
def bonjour():
    message = "Bonjour, je suis Théo \n"
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
