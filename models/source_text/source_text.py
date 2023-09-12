from models.source_text.words.words import Words


class SourceText:
    def __init__(self, session, user_input):
        self.session = session
        self.user_input = user_input
        french_and_english = self.session.openai_interface.get_french_and_english(
            self.user_input
        )
        self.french = french_and_english["french"]
        self.english = french_and_english["english"]
        print(f"\nFrench: {self.french}\nEnglish: {self.english}")
        self.words = Words(self)
