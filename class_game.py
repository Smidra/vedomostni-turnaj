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
        # Create secret word scramble
        self.secret_scramble = []
        j = 0
        for i in secret_word:
            j += 1
            self.secret_scramble.append(j)
        random.shuffle(self.secret_scramble)
        print(self.secret_word)
        print(self.secret_scramble)

    # -- METHODS --
    # Add new category 
    def add_category(self, category_text):
        new_category = class_category.Category(category_text)
        self.categories.append(new_category)
        return True
    
    # Change score of a team
    # Teams are assigned names for better readabikity of code
    def change_score(self, who, points):
        # Red = 1
        if who == 1:
            self.red_points += points
        # Blue = 2
        elif who == 2:
            self.blue_points += points

        return True

    # Get partial secret string for one of the teams
    # Red = 1
    # Blue = 2
    def get_partial_secret(self, who):
        # if who == 1:
        # for i in range(0, self.red_points):

                
        # if who == 2:

        return "TBA"

    # Load a new game from CSV file
    def load():
        return True
