import class_question

class Category:
    # -- ATTRIBUTES --
    # The point of the game is to guess the secret word
    def __init__(self, category_text):
        self.category_text = category_text
        self.questions = []

    # -- METHODS --
    # Add new question to category
    def add_question(self, text, answer):
        new_question = class_question.Question(text,answer)
        self.questions.append(new_question)
        return True

    def add_question(self, question):
        self.questions.append(question)
        return True
