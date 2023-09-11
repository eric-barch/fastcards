from apis.anki_interface import AnkiInterface
from apis.openai_interface import OpenAiInterface
from models.session import Session
from models.user_interface import UserInterface


def main():
    session = Session()
    session.user_interface.choose_deck()
    session.user_interface.request_input()


if __name__ == "__main__":
    main()
