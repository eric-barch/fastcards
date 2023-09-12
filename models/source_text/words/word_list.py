import json
from models.source_text.words.word_details import WordDetails


class WordList(list):
    def __init__(self, session, french_string):
        super().__init__()
        self.session = session
        self.french_string = french_string
        self.deconstruct_french_string()
        self.create_word_objects()

    def deconstruct_french_string(self):
        self.deconstructed_french_string = (
            self.session.openai_interface.deconstruct_french_string(self.french_string)
        )
        print(f"\ndeconstructed_french_string: {self.deconstructed_french_string}")

    def create_word_objects(self):
        responses = self.session.openai_interface.get_word_details(
            self.deconstructed_french_string,
        )

        print(json.dumps(responses, indent=2))

        # for response in responses:
        #     word_details = WordDetails(
        #         self.session,
        #         self,
        #         response["french"],
        #         response["english"],
        #         response["part_of_speech"],
        #         response["is_masculine"],
        #     )
        #     self.append(word_details)
