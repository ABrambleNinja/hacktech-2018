class Game:
    ''' Each game will be an instance of this object '''
    def __init__(self, num_people, fancy=True,
                 location_type="random", time_limit=0):
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

    def join_game(self):
        ''' Allows a new person to join the game '''

        # When a new person joins a game, we need to increment the number of
        # people in the game, and then give them a role that is available
        if self.current_players < self.num_people:
            if self.current_players == self.spy_id:
                self.player_dictionary[self.current_players] = ["Spy", None]
                self.current_players += 1
                return ("Spy", "UNKNOWN")
            else:
                role = self.available_roles[self.current_players]
                if (self.fancy):
                    role = self.fancify_role(role)
                self.player_dictionary[self.current_players] = [role, None]
                self.current_players += 1
                return (role, self.location)
        else:
            abort(404, description="Too Many People in Game")

    def fancify_role(self, role):
        ''' Takes a regular role and makes it fancies '''
        color = random.choice(DATA.colors_list)
        adjective = random.choice(DATA.adjectives_list)
        return color + " " + adjective[0].upper() + adjective[1:] + " " + role

    def set_custom_location(self, location, roles):
        ''' Allows the player to put in a custom location with associated
        roles.
        @params:
        location - String
        roles - List'''
        pass

    def make_guess(self, layer_guessing, guess):
        '''
        Allows a single user to make a guess for who they think the
        spy is.
        '''
        self.player_dictionary[player_guessing][1] = guess

    def checkGameOver(self):
        '''
        Checks if the game is over
        '''
        timesAccused = [0 for i in range(self.num_people)]

        print(self.player_dictionary)
        for player_id, player_tuple in self.player_dictionary:
            timesAccused[player_tuple[1]] += 1

        for num in timesAccused:
            if num >= self.num_people:
                return "Win"
        return "Loss"


    @staticmethod
    def next_game_id():
        ''' Gets the index of the game array to insert the new game,
         or returns None if it should be appended '''
        for i in range(len(DATA.games)):
            if DATA.games[i] == None:
                return i
        return None
