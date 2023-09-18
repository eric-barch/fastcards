from interfaces.user import User
from interfaces.anki import Anki
from interfaces.openai import OpenAi


class Session:
    def __init__(self):
        self.user = User(self)
        self.anki = Anki(self)
        self.openai = OpenAi(self)
        self.text = None
        self.notes = None
