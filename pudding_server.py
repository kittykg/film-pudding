from flask import Flask, request

app = Flask(__name__)


@app.route('/health-probe')
def hello_pudding():
    return 'Hello from pudding!'
