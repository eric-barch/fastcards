from models.user_interface import UserInterface
from apis.anki_interface import AnkiInterface
from apis.openai_interface import OpenAiInterface


class Session:
    def __init__(self):
        self.user_interface = UserInterface(self)
        self.anki_interface = AnkiInterface(self)
        self.openai_interface = OpenAiInterface(self)
        self.translation = None
