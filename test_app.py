#!/usr/bin/env python3
"""
Simple test Flask app
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello SnapStudio!</h1><p>Your Flask app is working!</p>'

if __name__ == '__main__':
    print("Starting simple Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
