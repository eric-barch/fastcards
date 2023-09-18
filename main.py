from models.session import Session
from models.text.text import Text
from models.text.notes.notes import Notes


def main():
    session = Session()

    exit = False

    while not exit:
        read_deck_name, write_deck_name = session.user_interface.select_deck_names()
        session.anki_interface.read_deck_name = read_deck_name
        session.anki_interface.write_deck_name = write_deck_name

        restart = False

        while not restart:
            text = session.user_interface.enter_text()

            if text.lower().strip() == "restart":
                restart = True
                break

            if text.lower().strip() == "exit":
                exit = True
                break

            session.text = Text(session, text)
            session.notes = Notes(session)

            selected_note_indices = session.user_interface.select_new_notes()

            print(f"\nAdding these notes:\n")
            for selected_note_index in selected_note_indices:
                print(session.notes[selected_note_index])


if __name__ == "__main__":
    main()
