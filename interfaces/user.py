from models.source_string.source_string import SourceString


class UserInterface:
    def __init__(self, session):
        self.session = session

    def choose_decks(self):
        read_deck_name = self.choose_deck("Choose a deck to check for existing notes: ")
        print(f"\nRead deck selected: {read_deck_name}")
        self.session.anki_interface.read_deck_name = read_deck_name

        write_deck_name = self.choose_deck("Choose a deck to add new notes to: ")
        print(f"\nWrite deck selected: {write_deck_name}")
        self.session.anki_interface.write_deck_name = write_deck_name

    def choose_deck(self, prompt):
        all_deck_names = self.session.anki_interface.get_all_deck_names()

        print("\nAll decks:\n")

        for i, deck_name in enumerate(all_deck_names, start=1):
            print(f"{i}. {deck_name}")

        while True:
            user_input = input(f"\n{prompt}")

            try:
                choice = int(user_input)
            except:
                print("\nPlease enter a valid number.")
                continue

            try:
                deck_name = all_deck_names[choice - 1]
                return deck_name
            except:
                print("\nInvalid choice. Please select a number from the list.")
                continue

    def process_french_string(self):
        while True:
            user_input = input(
                "\nEnter a string in French (or type 'exit' to quit):\n\n"
            )

            if user_input == "exit":
                break

            self.session.source_string = SourceString(self.session, user_input)

            notes_to_create = self.request_notes_to_create()

            print(f"\n{notes_to_create}")

    def request_notes_to_create(self):
        while True:
            user_input = input(
                "\nEnter the number(s) of the note(s) you want to create, separated by commas "
                + "(or type 'a' to create a note for all non-existent, non-proper nouns):\n\n"
            )

            potential_notes = self.session.source_string.potential_notes
            notes_to_create_indices = []

            if user_input.lower().strip() == "a":
                for i, potential_note in enumerate(potential_notes):
                    notes_to_create_indices.append(i)
                return notes_to_create_indices

            try:
                user_input_indices = [(int(i) - 1) for i in user_input.split(",")]

                for i in user_input_indices:
                    if i < 0 or i >= len(potential_notes):
                        raise Exception

                return user_input_indices
            except:
                print("\nInvalid input.")
                continue
