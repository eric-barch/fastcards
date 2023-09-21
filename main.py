from models.session import Session
from models.text.text import Text


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

            Text(session, text)

            selected_token_indices = session.user.select_tokens()


if __name__ == "__main__":
    main()
