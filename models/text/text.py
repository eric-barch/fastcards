class Text:
    def __init__(self, session, text):
        self.session = session
        self.user_input = text

        source_and_target = self.session.openai_interface.get_source_and_target(
            self.user_input
        )

        self.source = source_and_target["source"]
        print(f"\nsource: {self.source}")

        self.target = source_and_target["target"]
        print(f"target: {self.target}")
