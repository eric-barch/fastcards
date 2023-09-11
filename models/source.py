class Source:
    def __init__(self, session, input):
        self.session = session
        self.input = input
        self.french = self.session.openai_interface.get_clean_french(input)
        print(f"French: {self.french}")
        self.english = self.session.openai_interface.get_english_translation(
            self.french
        )
        print(f"English: {self.english}")
        # self.words = Words(self)
