# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_falsk():
    keyword_test = "테스트문자"
    size = 50
    return render_template('NewFile.html',keyword_test = keyword_test,size=size)
@app.route('/<keyword>/<size>')
def hello_falsk2(keyword,size):
    keyword_test = keyword
    size = size
    return render_template('NewFile.html',keyword_test = keyword_test,size=size)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

