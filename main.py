from interfaces.anki_interface import AnkiInterface
from interfaces.user_interface import UserInterface
from interfaces.open_ai_interface import OpenAiInterface
from models.text import Text


def main():
    anki_interface = AnkiInterface()
    user_interface = UserInterface()
    open_ai_interface = OpenAiInterface()

    exit = False

    while not exit:
        all_deck_names = anki_interface.get_all_deck_names()
        read_deck_name, write_deck_name = user_interface.select_decks(all_deck_names)
        anki_interface.set_deck_names(read_deck_name, write_deck_name)

        restart = False

        while not restart:
            input = user_interface.enter_input()

            if input.lower().strip() == "restart":
                restart = True
                break

            if input.lower().strip() == "exit":
                exit = True
                break

            text = Text(input)

            anki_interface.find_existing_notes(text)
            token_indices = user_interface.select_tokens(text)

            if not token_indices:
                continue

            open_ai_interface.look_up_tokens(text)
            user_interface.select_notes(text)
            anki_interface.add_notes(text)


if __name__ == "__main__":
    main()
