import inquirer

from global_variables import source_language


class UserInterface:
    def __init__(self):
        pass

    def select_decks(self, available_deck_names):
        read_deck_name = self.select_deck("Select read deck", available_deck_names)
        write_deck_name = self.select_deck("Select write deck", available_deck_names)
        return read_deck_name, write_deck_name

    def select_deck(self, prompt, available_deck_names):
        print()

        questions = [
            inquirer.List(
                name="deck_name",
                message=prompt,
                choices=available_deck_names,
            ),
        ]

        return inquirer.prompt(questions).get("deck_name")

    def enter_input(self):
        return input(
            f"Enter a string in {source_language.capitalize()} ('restart' to change decks, 'exit' to quit):\n\n"
        )

    def select_tokens(self, text):
        print()

        tokens = text.tokens
        choices = [(str(token), i) for i, token in enumerate(tokens)]
        default_choices = [
            i
            for i, token in enumerate(tokens)
            if not token.get_notes() and token.pos != "PROPN"
        ]

        questions = [
            inquirer.Checkbox(
                name="token_indices",
                message="Select tokens to look up",
                choices=choices,
                default=default_choices,
            ),
        ]

        token_indices = inquirer.prompt(questions).get("token_indices")

        for index in token_indices:
            tokens[index].will_look_up = True

        return token_indices

    def select_notes(self, text):
        print()

        new_notes = text.get_new_notes()
        choices = [(str(note), i) for i, note in enumerate(new_notes)]
        default_choices = [i for _, i in choices]

        questions = [
            inquirer.Checkbox(
                name="new_note_indices",
                message="Select notes to create",
                choices=choices,
                default=default_choices,
            )
        ]

        new_note_indices = inquirer.prompt(questions).get("new_note_indices")

        for index in new_note_indices:
            new_notes[index].will_add = True
