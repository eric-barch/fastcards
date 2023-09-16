from .potential_note_list.potential_note_list import PotentialNoteList


class SourceString:
    def __init__(self, session, user_input):
        self.session = session
        self.user_input = user_input

        french_and_english_strings = (
            self.session.openai_interface.get_french_and_english_strings(
                self.user_input
            )
        )

        self.french_string = french_and_english_strings["french"]
        print(f"\nfrench_string: {self.french_string}")

        self.english_string = french_and_english_strings["english"]
        print(f"english_string: {self.english_string}\n")

        self.potential_note_list = PotentialNoteList(
            self.session,
            self.french_string,
        )
