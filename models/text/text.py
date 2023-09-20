class Text:
    def __init__(self, session, text):
        self.session = session
        self.text = text

        source_and_target = self.session.openai.get_text_source_and_target(self.text)

        self.source = source_and_target["source"]
        print(f"\nsource: {self.source}")

        self.target = source_and_target["target"]
        print(f"target: {self.target}")
