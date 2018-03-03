import json
import pprint
import random

from flask import Flask, render_template

app = Flask(__name__)

games = []


class Data:
    def __init__(self):
        self.debugging = True
        app.config['DEBUG'] = self.debugging
        self.adjectives_list = []
        self.colors_list = []
        self.locations_dict = {}

    def load_json_adjectives(self):
        json_data = open("info.json").read()
        data = json.loads(json_data)
        self.adjectives_list = data["adjectives"]
        self.colors_list = data["colors"]

    def load_json_roles(self):
        '''
        Gets all of the location and role data from the JSON file
        '''
        json_data = open("locations.json").read()
        self.locations_dict = json.loads(json_data)


class Game:
    ''' Each game will be an instance of this object '''
    def __init__(self, num_people, fancy=True):
        ''' Initializer for a new game '''
        self.num_people = num_people
        self.current_players = 0
        self.location = get_location()
        self.available_roles = get_roles(location)
        self.player_dictionary = {player_id: role for player_id, role in
                                  zip(list(range(num_people)), roles)}
        self.fancy = fancy

    def update_size(self, num_people):
        ''' Change the number of people currently in the game '''
        self.num_people = num_people

    def join_game(self, ):
        ''' Allows a new person to join the game '''
        self.current_players += 1

    def set_custom_location(location, roles):
        ''' Allows the player to put in a custom location with associated
        roles.
        @params:
        location - String
        roles - List'''
        pass

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
    return render_template('index.html')

@app.route('/game/<id>')
def game():
    ''' '''
    pass

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/role_test')
def get_some_role():
    return get_role(get_location())


def get_location():
    ''' Returns a random location from the set of possible values '''
    return random.choice(list(DATA.locations_dict.keys()))


def get_role(location, fancy=True):
    ''' Given a location, returns one of the possible roles from the location.
    If fancy is enabled, this will also choose some color and an adjective '''
    role = random.choice(DATA.locations_dict[location])
    if (fancy):
        color = random.choice(DATA.colors_list)
        adjective = random.choice(DATA.adjectives_list)
        return color + " " + adjective[0].upper() + adjective[1:] + " " + role
    else:
        return role


def testing():
    ''' A function used on startup if in debugging mode '''
    print("In debugging mode")
    print(get_role(get_location(), True))

if __name__ == "__main__":
    DATA = Data()
    DATA.load_json_adjectives()
    DATA.load_json_roles()

    if DATA.debugging:
        testing()

    app.run(host='0.0.0.0')
