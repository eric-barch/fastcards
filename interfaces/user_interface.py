import inquirer


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
        user_input = input(
            "\nEnter a string in the source language ('restart' to change decks, 'exit' to quit):\n\n"
        )
        return user_input

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

        marked_indices = inquirer.prompt(questions).get("tokens")

        for index in marked_indices:
            tokens[index].marked_for_lookup = True
