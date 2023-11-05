import inquirer

from global_vars import source_language


class UserInterface:
    def __init__(self):
        pass

    def select_decks(self, available_decks):
        read_deck_name = self.select_deck("Select read deck", available_decks)
        write_deck_name = self.select_deck("Select write deck", available_decks)
        return read_deck_name, write_deck_name

    def select_deck(self, prompt, available_decks):
        print()

        questions = [
            inquirer.List(
                name="deck",
                message=prompt,
                choices=available_decks,
            ),
        ]

        return inquirer.prompt(questions).get("deck")

    def enter_input(self):
        return input(
            f"Enter a string in {source_language} ('restart' to change decks, 'exit' to quit):\n\n"
        )

    def select_tokens(self, text):
        print()

        tokens = text.tokens

        questions = [
            inquirer.Checkbox(
                name="tokens",
                message="Select tokens to look up",
                choices=[(str(token), i) for i, token in enumerate(tokens)],
                default=[
                    (i)
                    for i, token in enumerate(tokens)
                    if not token.notes and token.pos != "PROPN"
                ],
            ),
        ]

        indices = inquirer.prompt(questions).get("tokens")

        for index in indices:
            tokens[index].will_look_up = True

    def select_notes(self, text):
        print()

        new_notes = text.get_new_notes()

        questions = [
            inquirer.Checkbox(
                name="notes",
                message="Confirm notes to create",
                choices=[(str(note), i) for i, note in enumerate(new_notes)],
                default=[(i) for i, note in enumerate(new_notes)],
            )
        ]

        indices = inquirer.prompt(questions).get("notes")

        for index in indices:
            new_notes[index].will_add = True
