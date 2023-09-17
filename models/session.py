from interfaces.user import UserInterface
from interfaces.anki import AnkiInterface
from interfaces.openai import OpenAiInterface


class Session:
    def __init__(self):
        self.user_interface = UserInterface(self)
        self.anki_interface = AnkiInterface(self)
        self.openai_interface = OpenAiInterface(self)
