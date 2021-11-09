import class_category
import random

class Game:
    # -- ATTRIBUTES --
    # The point of the game is to guess the secret word
    def __init__(self, secret_word):
        self.secret_word = secret_word
        self.categories = []
        self.red_points = 0
        self.blue_points = 0
        # Calculate max points from the length of secret word.
        self.max_points = len(secret_word)
        # Create secret word scramble letters for both teams in the same way.
        self.secret_scramble = []
        j = 0
        for i in secret_word:
            j += 1
            self.secret_scramble.append(j)
        random.shuffle(self.secret_scramble)

    # -- METHODS --
    # Add new category 
    def add_category(self, category_text):
        new_category = class_category.Category(category_text)
        self.categories.append(new_category)
        return True
    
    # Change score of a team
    # Teams are assigned names for better readability of code
    def change_score(self, who, points):
        # Red = 1
        if (who == 1) and (self.red_points < self.max_points):
            self.red_points += points
        # Blue = 2
        elif (who == 2) and (self.blue_points < self.max_points):
            self.blue_points += points

        return True

    # Get partial secret string for one of the teams
    def get_partial_secret(self, who):
        partial_secret = ["*" for i in range(len(self.secret_word))]
        print(self.secret_word)
        print(self.secret_scramble)
        print(partial_secret)

        # RED
        if who == 1:
            for i in range(0, self.red_points):
                partial_secret[ self.secret_scramble[i] -1 ] = self.secret_word[ self.secret_scramble[i] -1 ]
        # BLUE
        if who == 2:
            for i in range(0, self.blue_points):
                partial_secret[ self.secret_scramble[i]-1 ] = self.secret_word[ self.secret_scramble[i] -1 ]

        print(partial_secret)
        return_string = ''.join(map(str, partial_secret))
        return return_string

    # Load a new game from CSV file
    def load():
        return True
