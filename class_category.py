import class_question

# Class objects represent a single category from the game
class Category:
    # -- ATTRIBUTES --
    # The point of the game is to guess the secret word
    def __init__(self, category_text):
        self.category_text = category_text
        self.questions = []
        self.nr_questions = 0

    # -- METHODS --
    # Add new question to category
    def add_question(self, text, answer):
        new_question = class_question.Question(text,answer)
        self.questions.append(new_question)
        self.nr_questions += 1
        return True