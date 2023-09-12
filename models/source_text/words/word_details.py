import json


class WordDetails:
    def __init__(
        self,
        session,
        word_list,
        french,
    ):
        self.session = session
        self.word_list = word_list
        self.french = french

        response = session.openai_interface.get_word_details(french)

        self.english = response["english"]
        self.part_of_speech = response["part_of_speech"]
        self.gender = response["gender"]

        print(f"{self}")

    def __repr__(self):
        return json.dumps(
            {
                "french": self.french,
                "english": self.english,
                "part_of_speech": self.part_of_speech,
                "gender": self.gender,
            },
            indent=2,
        )
