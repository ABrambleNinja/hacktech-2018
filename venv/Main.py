from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    ''' Index of the Page '''
    return "Hello, World"


def get_location():
    ''' '''
    return "sample location"


def get_person():
    ''' '''
    return