from apis.anki_interface import AnkiInterface
from apis.openai_interface import OpenAiInterface
from models.session import Session
from models.user_interface import UserInterface


def main():
    session = Session()

    user_interface = UserInterface(session)
    anki_interface = AnkiInterface(session)
    openai_interface = OpenAiInterface(session)

    user_interface.choose_deck()
    user_interface.request_input()


if __name__ == "__main__":
    main()
