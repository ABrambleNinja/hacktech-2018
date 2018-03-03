import json
import pprint
import random
import os

from flask import Flask, session, render_template, request, url_for, abort

app = Flask(__name__)
playerList = {}

class Data:
    def __init__(self):
        ''' Initializes all of the data storage objects for the
        flask application '''
        app.secret_key = os.urandom(24)
        self.GAME_CAP = 10
        self.DEFAULT_SIZE = 5

        self.debugging = True
        app.config['DEBUG'] = self.debugging
        self.adjectives_list = []
        self.colors_list = []
        self.locations_dict = {}
        self.games = []

    def load_json_adjectives(self):
        ''' Loads all of the adjectives and colors from the external info.JSON
        file. Should only be done once per session. '''
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
    def __init__(self, num_people, fancy=True, location_type="random", time_limit=0):
        ''' Initializer for a new game '''
        self.num_people = num_people
        self.current_players = 0
        if location_type == "random":
            self.location = get_location()
        # When the game starts, all of the roles are available
        self.available_roles = DATA.locations_dict[self.location]
        self.player_dictionary = {}
        self.fancy = fancy
        # TODO: add support for more than one spy, and allow user to put in how many spies
        # they would like to have
        self.num_spies = 0
        self.num_max_spies = 1
        self.spy_id = -1
        random.shuffle(self.available_roles)
        self.pick_spy()
        self.time_limit = time_limit

    def pick_spy(self):
        ''' Decides which people will be the spies '''
        self.spy_id = random.randint(0, self.num_people-1)
        self.num_spies += 1

    def update_size(self, num_people):
        ''' Change the number of people currently in the game '''
        self.num_people = num_people

    def join_game(self, gameid):
        ''' Allows a new person to join the game '''
        if session['gameid'] == gameid: # person is already here
            return (self.player_dictionary[session['userid']], self.location)

        session['gameid'] = gameid
        session['playerid'] = self.current_players

        # When a new person joins a game, we need to increment the number of
        # people in the game, and then give them a role that is available
        if self.current_players < self.num_people:
            if self.current_players == self.spy_id:
                self.player_dictionary[self.current_players] = "Spy"
                self.current_players += 1
                return ("Spy", "UNKNOWN")
            else:
                role = self.available_roles[self.current_players]
                if (self.fancy):
                    role = self.fancify_role(role)
                self.player_dictionary[self.current_players] = role
                self.current_players += 1
                return (role, self.location)
        else:
            abort(404, description="Too Many People in Game")

    def fancify_role(self, role):
        ''' Takes a regular role and makes it fancies '''
        color = random.choice(DATA.colors_list)
        adjective = random.choice(DATA.adjectives_list)
        return color + " " + adjective[0].upper() + adjective[1:] + " " + role

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
def hello_world():
    ''' Index of the Page '''
    return render_template('index.html' )

def index_page():
    ''' Renders the home page of the website '''
    return render_template('index.html', default_people=DATA.DEFAULT_SIZE)


@app.route('/newgame', methods=["POST"])
def new_game():
    ''' Creates a new game '''
    # make new game
    L = request.get_json()
    isFancy = L[1]
    try:
        num_players = int(L[0])
    except:
        num_players = DATA.DEFAULT_SIZE

    location_type = L[2]
    time_limit = L[3]

    if (len(DATA.games) < DATA.GAME_CAP):
        # Initialize the game
        newGame = Game(num_players, isFancy, location_type, time_limit)
        # Find new game location (available ID)
        indexValue = Game.next_game_id()

        # Add the game in the right ID location
        if indexValue is None:
            # If indexValue is None, we must add more slots
            DATA.games.append(newGame)
            indexValue = len(DATA.games) - 1
        else:
            # Otherwise, we can add it to the regular location
            DATA.games[indexValue] = newGame

        # Return the ID of the game to the player (to get URL)
        return json.dumps(indexValue)
    else:
        return json.dumps("Cannot Create More Games")


@app.route('/game/<int:id_num>')
def join_game(id_num):
    ''' Connects user to existing game - if possible '''
    if (id_num >= len(DATA.games) or (DATA.games[id_num] is None)):
        abort(404, description="Not a Valid Game")
    else:
        game = DATA.games[int(id_num)]
        role, location = game.join_game(int(id_num))

    return render_template("game.html", gameID=id_num,
                           numPlayers=game.current_players,
                           role=role,
                           maxPlayers=game.num_people,
                           location=location,
                           time=game.time_limit)


@app.route('/gpsdata', methods=["POST"])
def gpsdata():
    ''' Gets GPS coordinates from the user, appends to the list'''
    data = request.data
    print(data)
    return json.dumps("this is the return thingy")

@app.route('/userID', methods=["POST"])
def iddata():
    ''' Gets ID from the user'''
    data = request.data
    print(data)
    return json.dumps("this is the test")

def addGPS():
    ''' Adds the user's location to the database of lists '''
    return playerList
    pass

def calculateDist(userloc,x):
    '''Finds all the locations in the list that are within x miles of user'''

    pass


@app.errorhandler(404)
def page_not_found(description):
    return render_template('404.html', desc=description)

@app.route('/role_test')
def get_some_role():
    return get_role(get_location())


def get_location():
    ''' Returns the user's location from the set of possible values '''
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
