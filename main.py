from models.session import Session
from models.source_string.source_string import SourceString


def main():
    session = Session()

    exit = False

    while not exit:
        restart = False

        read_deck_name, write_deck_name = session.user_interface.request_deck_names()
        session.anki_interface.read_deck_name = read_deck_name
        session.anki_interface.write_deck_name = write_deck_name

        while not restart:
            user_input = session.user_interface.request_source_language_string()

            if user_input.lower().strip() == "restart":
                restart = True
                break

            if user_input.lower().strip() == "exit":
                exit = True
                break

            session.source_string = SourceString(session, user_input)

            user_input = session.user_interface.request_new_notes()


if __name__ == "__main__":
    main()
