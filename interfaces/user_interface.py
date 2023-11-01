import inquirer


class UserInterface:
    def __init__(self):
        pass

    def select_decks(self, available_decks):
        read_deck_name = self.select_deck(
            "Choose a deck to read for existing notes: ", available_decks
        )
        print(f"\nRead deck selected: {read_deck_name}")

        write_deck = self.select_deck(
            "Choose a deck to write new notes to: ", available_decks
        )
        print(f"\nWrite deck selected: {write_deck}")

        return read_deck_name, write_deck

    def select_deck(self, prompt, available_decks):
        print("\nAll decks:\n")

        for i, deck_name in enumerate(available_decks, start=1):
            print(f"{i}. {deck_name}")

        while True:
            user_input = input(f"\n{prompt}")

            result = self.validate_deck_selection(user_input, len(available_decks))

            if result:
                return available_decks[result - 1]

    def validate_deck_selection(self, user_input, max_value):
        try:
            choice = int(user_input)
        except:
            print("\nPlease enter a valid number.")
            return None

        if choice < 1 or choice > max_value:
            print(f"\nInvalid choice. Please select a number from the list.")
            return None

        return choice

    def enter_input(self):
        user_input = input(
            "\nEnter a string in the source language ('restart' to change decks, 'exit' to quit):\n\n"
        )
        return user_input

    def mark_tokens_for_lookup(self, text):
        print()

        tokens = text.tokens

        questions = [
            inquirer.Checkbox(
                name="tokens",
                message="Mark tokens for lookup",
                choices=[(str(token), i) for i, token in enumerate(tokens)],
            ),
        ]

        marked_indices = inquirer.prompt(questions).get("tokens")

        for index in marked_indices:
            tokens[index].marked_for_lookup = True
