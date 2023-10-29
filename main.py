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
            input = session.user.enter_input()

            if input.lower().strip() == "restart":
                restart = True
                break

            if input.lower().strip() == "exit":
                exit = True
                break

            Text(session, input)

            # selected_token_indices = session.user.select_tokens()

            # session.text.add_notes(selected_token_indices)


if __name__ == "__main__":
    main()
