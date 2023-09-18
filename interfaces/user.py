class UserInterface:
    def __init__(self, session):
        self.session = session

    def request_deck_names(self):
        read_deck_name = self.request_deck_name(
            "Choose a deck to read for existing notes: "
        )
        print(f"\nRead deck selected: {read_deck_name}")

        write_deck_name = self.request_deck_name(
            "Choose a deck to write new notes to: "
        )
        print(f"\nWrite deck selected: {write_deck_name}")

        return {"read_deck_name": read_deck_name, "write_deck_name": write_deck_name}

    def request_deck_name(self, prompt):
        all_deck_names = self.session.anki_interface.get_all_deck_names()

        print("\nAll decks:\n")

        for i, deck_name in enumerate(all_deck_names, start=1):
            print(f"{i}. {deck_name}")

        while True:
            user_input = input(f"\n{prompt}")

            result = self.validate_deck_name_input(user_input, len(all_deck_names))

            if result:
                return result

    def validate_deck_name_input(self, user_input, max_value):
        try:
            choice = int(user_input)
        except:
            print("\nPlease enter a valid number.")
            return None

        if choice < 1 or choice > max_value:
            print(f"\nInvalid choice. Please select a number from the list.")
            return None

        return choice

    def request_source_language_string(self):
        user_input = input(
            "\nEnter a string in French ('restart' to change decks, 'exit' to quit):\n\n"
        )
        return user_input

    def request_new_notes(self):
        potential_notes = self.session.source_string.potential_notes

        print(f"\nPotential Notes: {potential_notes}")

        while True:
            user_input = input(
                "\nEnter the number(s) of the note(s) you want to create, separated by commas "
                "(or type 'a' to create a note for all non-existent, non-proper nouns):\n\n"
            )

            result = self.validate_new_notes_input(user_input, len(potential_notes))

            if result:
                return result

    def validate_new_notes_input(self, user_input, max_value):
        if user_input.lower().strip() == "a":
            return "a"

        try:
            user_input_indices = [int(i) for i in user_input.split(",")]

            # Check if the indices are within the valid range
            if any(i < 1 or i > max_value for i in user_input_indices):
                print(
                    f"\nInvalid. One or more of your choices falls outside the range of "
                    f"Potential Notes (1-{max_value})."
                )
                return None

            return user_input_indices

        except ValueError:
            print(
                "\nPlease enter 'a' or a comma-separated list of integers specifying the new notes "
                "you want to create."
            )
            return None
