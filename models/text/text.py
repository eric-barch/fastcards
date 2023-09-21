from models.text.tokens.tokens import Tokens


class Text:
    def __init__(self, session, text):
        self.session = session
        session.text = self

        self.text = text
        self.source, self.target = self.session.openai.get_source_and_target(self.text)

        print(f"\nsource: {self.source}")
        print(f"target: {self.target}")

        self.tokens = Tokens(self.session)
