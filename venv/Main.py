import json
import pprint
import random
import os

from flask import Flask, session, render_template, request, url_for, abort, session
from Data import Data
from Game import Game

app = Flask(__name__)
playerList = {}

@app.route('/')
def hello_world():
    ''' Index of the Page '''
    return render_template('index.html' )


def index_page():
    ''' Renders the home page of the website '''
    return render_template('index.html', default_people=DATA.DEFAULT_SIZE)


@app.route('/checkGameOver', methods=["POST"])
def check_game_over():
    ''' Given a game ID, checks if the spy was discovered or not based on
    the current. '''
    game_id = request.get_json()
    game = DATA.games[int(game_id)]
    status = game.checkGameOver()
    return json.dumps(status)

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


def calculateDist(userloc, x):
    '''Finds all the locations in the list that are within x miles of user'''
    pass


@app.errorhandler(404)
def page_not_found(description):
    return render_template('404.html', desc=description)


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
    app.secret_key = os.urandom(24)
    debugging = True
    app.config['DEBUG'] = debugging

    DATA = Data()
    DATA.load_json_adjectives()
    DATA.load_json_roles()
    DATA.debugging = debugging



    if DATA.debugging:
        testing()

    app.run(host='0.0.0.0')
