import json
import pprint
import random

from flask import Flask, session, render_template, request, url_for, abort

app = Flask(__name__)


class Data:
    def __init__(self):
        ''' '''
        self.GAME_CAP = 10
        self.DEFAULT_SIZE = 5

        self.debugging = True
        app.config['DEBUG'] = self.debugging
        self.adjectives_list = []
        self.colors_list = []
        self.locations_dict = {}
        self.games = []

    def load_json_adjectives(self):
        ''' '''
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
        # When the game starts, all of the roles are available
        self.available_roles = DATA.locations_dict[self.location]
        self.player_dictionary = {player_id: role for player_id, role in
                                  zip(list(range(num_people)),
                                  self.available_roles)}
        self.fancy = fancy

    def update_size(self, num_people):
        ''' Change the number of people currently in the game '''
        self.num_people = num_people

    def join_game(self):
        ''' Allows a new person to join the game '''

        # When a new person joins a game, we need to increment the number of
        # people in the game, and then give them a role that is available

        # TODO: make sure there aren't too many people in the game
        # TODO: make sure that people get unique roles
        if self.current_players < self.num_people:
            self.current_players += 1
            role, fancy_role = get_role(self.location, self.fancy)
            return fancy_role
        else:
            abort(404, description="Too Many People in Game")

    def set_custom_location(location, roles):
        ''' Allows the player to put in a custom location with associated
        roles.
        @params:
        location - String
        roles - List'''
        pass

    def make_guess():
        '''
        Allows a single user to make a guess for who they think the
        spy is.
        '''
        pass

    def game_over():
        '''
        Checks if the game is over
        '''
        pass

    @staticmethod
    def next_game_id():
        ''' Gets the index of the game array to insert the new game,
         or returns None if it should be appended '''
        for i in range(len(DATA.games)):
            if DATA.games[i] == None:
                return i
        return None

@app.route('/')
def index_page():
    ''' Renders the home page of the website '''
    return render_template('index.html')

@app.route('/newgame', methods=["POST"])
def new_game():
    ''' Creates a new game '''
    # make new game
    L = request.get_json()
    try:
        num_players = int(L)
        print('got num players')
    except:
        # TODO: handle this
        num_players = DATA.DEFAULT_SIZE

    if (len(DATA.games) < DATA.GAME_CAP):
        newGame = Game(num_players)
        # find new game location
        indexValue = Game.next_game_id()

        # add the game in the right place
        if indexValue is None:
            DATA.games.append(newGame)
            indexValue = len(DATA.games) - 1
        else:
            DATA.games[indexValue] = newGame

        # send it back
        return json.dumps(indexValue)
    else:
        return json.dumps("Cannot Create More Games")

@app.route('/game/<int:id_num>')
def game(id_num):
    ''' Connects user to existing game - if possible '''
    if (id_num >= len(DATA.games) or (DATA.games[id_num] is None)):
        abort(404, description="Not a Valid Game")
    else:
        game = DATA.games[id_num]
        info = game.join_game()

    return render_template("game.html", gameID=id_num, numPlayers=DATA.games[id_num].current_players, role=info)

@app.route('/gpsdata', methods = ["POST"])
def gpsdata():
    ''' Gets GPS coordinates from '''
    pprint(request.data)
    return "this is the return thingy"

@app.errorhandler(404)
def page_not_found(description):
    return render_template('404.html', desc = description)

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
        return (role, color + " " + adjective[0].upper() + adjective[1:] + " " + role)
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
