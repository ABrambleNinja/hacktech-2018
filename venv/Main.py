from flask import Flask
import json
import pprint

app = Flask(__name__)

debugging = True
app.config['DEBUG'] = debugging
adjectives_list = []
colors_list = []


class Game:
    ''' Each game will be an instance of this object '''
    def __init__(self, num_people):
        ''' Initializer for a new game '''
        self.num_people = num_people
        self.current_players = 0
        self.location = get_random_location()
        self.available_roles = get_roles(location)
        self.player_dictionary = {player_id: role for player_id, role in
                                  zip(list(range(num_people)), roles)}

    def update_size(self, num_people):
        ''' Change the number of people currently in the game '''
        self.num_people = num_people

    def join_game(self, ):
        ''' Allows a new person to join the game '''
        self.current_players += 1

@app.route('/')
def hello_world():
    ''' Index of the Page '''
    return "Hello, World"

@app.route('/game/<id>')
def game():
    ''' '''
    pass


def load_ajectives():
    json_data = open("info.json").read()
    data = json.loads(json_data)
    adjectives_list = data["adjectives"]
    colors_list = data["colors"]


def load_json_data():
    '''
    Gets all of the location and role data from the JSON file
    '''
    json_data = open(file_directory).read()
    data = json.loads(json_data)


def get_location():
    ''' '''
    return "sample location"


def get_person():
    ''' '''
    return


def testing():
    ''' A function used on startup if in debugging mode '''
    print("testing....")
    load_ajectives()


if __name__ == "__main__":
    if debugging:
        testing()

    app.run()
