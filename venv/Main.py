from flask import Flask
import json
import pprint

app = Flask(__name__)

@app.route('/')
def hello_world():
    ''' Index of the Page '''
    return "Hello, World"


def load_json_data():
    '''
    Gets all of the location and role data from the JSON file
    '''
    json_data=open(file_directory).read()
    data = json.loads(json_data)


def get_location():
    ''' '''
    return "sample location"


def get_person():
    ''' '''
    return