import json
import pprint
import random

from flask import Flask

app = Flask(__name__)

app.config['DEBUG'] = debugging
adjectives_list = []
colors_list = []
debugging = True
role_list = []
games = []


class Game:
    ''' Each game will be an instance of this object '''
    def __init__(self, num_people):
        ''' Initializer for a new game '''
        self.num_people = num_people
        self.current_players = 0
        self.location = get_location()
        self.available_roles = get_roles(location)
        self.player_dictionary = {player_id: role for player_id, role in
                                  zip(list(range(num_people)), roles)}

    def update_size(self, num_people):
        ''' Change the number of people currently in the game '''
        self.num_people = num_people

    def join_game(self, ):
        ''' Allows a new person to join the game '''
        self.current_players += 1

    @staticmethod
    def next_game_id():
        ''' Gets the index of the game array to insert the new game, or returns None if it should be appended '''
        for i in range(len(games)):
            if games[i] == None:
                return i
        return None

@app.route('/')
def hello_world():
    ''' Index of the Page '''
    return "Hello, World"

@app.route('/game/<id>')
def game():
    ''' '''
    pass


def load_json_ajectives():
    json_data = open("info.json").read()
    data = json.loads(json_data)
    adjectives_list = data["adjectives"]
    colors_list = data["colors"]


def load_json_roles():
    '''
    Gets all of the location and role data from the JSON file
    '''
    json_data = open(file_directory).read()
    data = json.loads(json_data)


def get_location():
    ''' '''
    return "sample location"


def get_role(fancy=True):
    ''' '''
    role = random.choice(role_list)
    if (fancy):
        color = random.choice(colors_list)
        adjective = random.choice(adjectives_list)
        return color + " " + adjective + " " + role
    else:
        return role


def testing():
    ''' A function used on startup if in debugging mode '''
    print("In debugging mode")

if __name__ == "__main__":
    load_json_ajectives()
    load_json_roles()
    if debugging:
        testing()

    app.run()
