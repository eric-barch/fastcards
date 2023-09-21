class User:
    def __init__(self, session):
        self.session = session

    def select_deck_names(self):
        read_deck_name = self.request_deck_name(
            "Choose a deck to read for existing notes: "
        )
        print(f"\nRead deck selected: {read_deck_name}")

        write_deck_name = self.request_deck_name(
            "Choose a deck to write new notes to: "
        )
        print(f"\nWrite deck selected: {write_deck_name}")

        return read_deck_name, write_deck_name

    def request_deck_name(self, prompt):
        all_deck_names = self.session.anki.get_all_deck_names()

        print("\nAll decks:\n")

        for i, deck_name in enumerate(all_deck_names, start=1):
            print(f"{i}. {deck_name}")

        while True:
            user_input = input(f"\n{prompt}")

            result = self.validate_deck_name_input(user_input, len(all_deck_names))

            if result:
                return all_deck_names[result - 1]

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

    def enter_text(self):
        user_input = input(
            "\nEnter a string in the source language ('restart' to change decks, 'exit' to quit):\n\n"
        )
        return user_input

    def select_tokens(self):
        tokens = self.session.text.tokens

        print(f"\nExtracted tokens:\n{tokens}")

        while True:
            user_input = input(
                "\nEnter the number(s) of the token(s) you want to create notes for, separated by "
                "commas or type 'a' for all (will skip duplicates and proper nouns):\n\n"
            )

            result = self.validate_new_tokens_input(user_input, len(tokens))

            if result:
                token_indices = []

                if result == "a":
                    for i, token in enumerate(tokens):
                        token_indices.append(i)
                else:
                    for token_number in result:
                        token_index = token_number - 1
                        token_indices.append(token_index)

                return token_indices

    def validate_new_tokens_input(self, user_input, max_value):
        if user_input.lower().strip() == "a":
            return "a"

        try:
            user_input_indices = [int(i) for i in user_input.split(",")]

            # Check if the indices are within the valid range
            if any(i < 1 or i > max_value for i in user_input_indices):
                print(
                    f"\nInvalid. One or more of your choices falls outside the range of "
                    f"Tokens (1-{max_value})."
                )
                return None

            return user_input_indices

        except ValueError:
            print(
                "\nPlease enter 'a' or a comma-separated list of integers specifying the new tokens "
                "you want to create."
            )
            return None
