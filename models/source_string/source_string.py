class SourceString:
    def __init__(self, session, user_input):
        self.session = session
        self.user_input = user_input

        source_and_target_strings = (
            self.session.openai_interface.get_source_and_target_strings(self.user_input)
        )

        self.source_string = source_and_target_strings["source"]
        print(f"\nsource_string: {self.source_string}")

        self.target_string = source_and_target_strings["target"]
        print(f"target_string: {self.target_string}")
