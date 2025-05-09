import class_category
import random
import pandas


class Game:
    # -- ATTRIBUTES --
    # The point of the game is to guess the secret word
    def __init__(self, secret_word):
        self.game_name = "No game name"
        self.categories = []
        self.red_points = 0
        self.blue_points = 0
        self.green_points = 0
        # Create secret word scramble - letters for both teams in the same way.
        self.secret_word = ""
        self.max_points = 0
        self.secret_scramble = []
        self.update_secret(secret_word)

    # -- METHODS --
    # Update secret word in this game
    def update_secret(self, new_secret_word):
        # Calculate max points from the length of secret word.
        self.max_points = len(new_secret_word)
        self.secret_word = new_secret_word  # Set secret word
        self.secret_scramble = []   # Delete old secret scramble
        # Create new secret scramble - same for both teams
        j = 0
        for i in new_secret_word:
            j += 1
            self.secret_scramble.append(j)
        random.shuffle(self.secret_scramble)
        return True

    # Add new category if it does not exist.
    def add_category(self, category_text):
        # Does it exist?
        if self.get_category_by_name(category_text) == False:
            new_category = class_category.Category(category_text)
            self.categories.append(new_category)
        else:
            return False
        return True

    # Get category by strng name
    def get_category_by_name(self, category_name):
        for cat in self.categories:
            if cat.category_text == category_name:
                return cat
        return False

    # Change score of a team
    # Score cannot be over maximum number of points
    def change_score(self, who, points):
        # Red = 1
        if (who == 1) and ((self.red_points < self.max_points) or (points < 0)):
            self.red_points += points
        # Blue = 2
        elif (who == 2) and ((self.blue_points < self.max_points) or (points < 0)):
            self.blue_points += points
        # Green = 3
        elif (who == 3) and ((self.green_points < self.max_points) or (points < 0)):
            self.green_points += points

        return True

    # Get partial secret string for one of the teams –
    def get_partial_secret(self, who):
        partial_secret = ["-" for i in range(len(self.secret_word))]
        # Red = 1
        if who == 1:
            for i in range(0, self.red_points):
                partial_secret[self.secret_scramble[i]-1] = self.secret_word[self.secret_scramble[i]-1]
        # Blue = 2
        if who == 2:
            for i in range(0, self.blue_points):
                partial_secret[self.secret_scramble[i]-1] = self.secret_word[self.secret_scramble[i]-1]
        # Green = 3
        if who == 3:
            for i in range(0, self.green_points):
                partial_secret[self.secret_scramble[i]-1] = self.secret_word[self.secret_scramble[i]-1]

        return_string = ''.join(map(str, partial_secret))
        return return_string

    # Load a new game from CSV file
    def load(self, game_csv_name):
        # Load csv file formatted as gamefile_sample.csv
        array_game = pandas.read_csv(game_csv_name, header=None).values
        self.categories = [] # Delete old game categories
        # Null points
        self.red_points = 0
        self.blue_points = 0
        self.green_points = 0
        # Game info
        self.game_name = array_game[0][1]
        self.update_secret(array_game[1][1])
        # Create game questions
        for i in range(5, len(array_game)):
            self.add_category(array_game[i][0])
            this_category = self.get_category_by_name(array_game[i][0])
            this_category.add_question(array_game[i][1], array_game[i][2])

        return True
