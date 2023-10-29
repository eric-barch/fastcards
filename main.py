from interfaces.anki_interface import AnkiInterface
from interfaces.user_interface import UserInterface
from models.tokens import Tokens


def main():
    anki_interface = AnkiInterface()
    user_interface = UserInterface()

    exit = False

    while not exit:
        all_decks = anki_interface.get_all_decks()
        read_deck, write_deck = user_interface.select_decks(all_decks)
        anki_interface.set_decks(read_deck, write_deck)

        restart = False

        while not restart:
            input = user_interface.enter_input()

            if input.lower().strip() == "restart":
                restart = True
                break

            if input.lower().strip() == "exit":
                exit = True
                break

            tokens = Tokens(input)

            anki_interface.check_for_existing_notes(tokens)
            user_interface.select_tokens_to_look_up(tokens)

            notes = openai_interface.define_tokens(input, tokens)

            anki_interface.add_notes(notes)


if __name__ == "__main__":
    main()
