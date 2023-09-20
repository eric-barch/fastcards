from models.session import Session
from models.text.text import Text
from models.text.tokens.tokens import Tokens


def main():
    session = Session()

    exit = False

    while not exit:
        read_deck_name, write_deck_name = session.user.select_deck_names()

        session.anki.read_deck_name = read_deck_name
        session.anki.write_deck_name = write_deck_name

        restart = False

        while not restart:
            text = session.user.enter_text()

            if text.lower().strip() == "restart":
                restart = True
                break

            if text.lower().strip() == "exit":
                exit = True
                break

            session.text = Text(session, text)
            session.tokens = Tokens(session)


if __name__ == "__main__":
    main()
