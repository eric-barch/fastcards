from interfaces.user_interface import UserInterface
from interfaces.anki_interface import AnkiInterface
from models.text import Text


def main():
    user_interface = UserInterface()

    exit = False
    while not exit:
        read_deck_name, write_deck_name = user_interface.select_deck_names()

        anki_interface = AnkiInterface(read_deck_name, write_deck_name)

        while not restart:
            input = user_interface.request_input()

            if input.lower().strip() == "restart":
                restart = True
                break

            if input.lower().strip() == "exit":
                exit = True
                break

            text = Text(session, input)

            # selected_token_indices = session.user.select_tokens()

            # session.text.add_notes(selected_token_indices)


if __name__ == "__main__":
    main()
