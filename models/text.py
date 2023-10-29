from models.tokens import Tokens


class Text:
    def __init__(self, session, input):
        self.session = session
        session.text = self

        self.input = input
        self.source, self.target = self.session.openai.get_source_and_target(self.input)

        print(f"\nsource: {self.source}")
        print(f"target: {self.target}")

        self.tokens = Tokens(self.session, self)

    def add_notes(self, selected_token_indices):
        for selected_token_index in selected_token_indices:
            token = self.tokens[selected_token_index]
            self.session.anki.add_note(
                token.note,
            )
