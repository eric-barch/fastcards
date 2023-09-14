import json


class PotentialNote:
    def __init__(self, session, french_string, token_datum):
        self.session = session
        self.french_string = french_string
        self.token_datum = token_datum
        self.set_front()
        self.get_note_details()
        # self.set_exists_in_anki()

    def set_front(self):
        is_contraction_part = self.token_datum["representation"].endswith("'")
        is_inverted_subject_pron = self.token_datum["representation"].startswith("-")
        is_verb = self.token_datum["pos"] == "verb"

        lemma_front = is_contraction_part or is_inverted_subject_pron or is_verb

        if lemma_front:
            self.front = self.token_datum["lemma"]
        else:
            self.front = self.token_datum["representation"]

        print(
            f"\nfront: {self.front:<15}pos: {self.token_datum['pos']:<15}lemma: {self.token_datum['lemma']:<15}"
        )

    def get_note_details(self):
        bracketed_french_string = self.bracket_french_string()

        print(bracketed_french_string)

        request_obj = {
            "string": bracketed_french_string,
            "french": self.front,
            "pos": self.token_datum["pos"],
        }
        request = json.dumps(request_obj)

        response = self.session.openai_interface.get_note_details(request)

        print(json.dumps(response, indent=4))

    def bracket_french_string(self):
        start = self.token_datum["start"]
        end = self.token_datum["end"]

        return (
            self.french_string[:start]
            + "["
            + self.french_string[start:end]
            + "]"
            + self.french_string[end:]
        )
