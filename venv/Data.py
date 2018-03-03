import json

class Data:
    def __init__(self):
        ''' Initializes all of the data storage objects for the
        flask application '''
        self.GAME_CAP = 10
        self.DEFAULT_SIZE = 5

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