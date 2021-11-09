class Question:
    # -- ATTRIBUTES --
    # The point of the game is to guess the secret word
    def __init__(self, question_text, question_answer):
        self.question_text = question_text
        self.question_answer = question_answer
        self.seen = False

    # -- METHODS --
    # Toggle seen to True
    def make_seen(self):
        self.seen = True
        return True
