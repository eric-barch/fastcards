import json
import urllib.request


class Anki:
    def __init__(self, session):
        self.session = session
        session.anki = self
        self.read_deck_name = None
        self.write_deck_name = None

    def call_api(self, action, **params):
        request = {"action": action, "params": params, "version": 6}
        requestJson = json.dumps(request).encode("utf-8")
        response = json.load(
            urllib.request.urlopen(
                urllib.request.Request("http://localhost:8765", requestJson)
            )
        )
        if len(response) != 2:
            raise Exception("Response has an unexpected number of fields.")
        if "error" not in response:
            raise Exception("Response is missing required error field.")
        if "result" not in response:
            raise Exception("Response is missing required result field.")
        if response["error"] is not None:
            raise Exception(response["error"])
        return response["result"]

    def get_all_deck_names(self):
        return self.call_api("deckNames")

    def find_notes_by_front(self, front):
        query = f'deck:"{self.read_deck_name}" "front:{front}"'

        return self.call_api(
            "findNotes",
            query=query,
        )

    def add_note(self, note):
        if note.gender == None:
            gender = "none"
        else:
            gender = note.gender

        if note.number == None:
            number = "none"
        else:
            number = note.number

        return self.call_api(
            "addNote",
            note={
                "deckName": self.write_deck_name,
                "modelName": "Forward and Reverse with Grammatical Detail (Type Answer)",
                "fields": {
                    "Front": note.front,
                    "Back": note.back,
                    "Part of Speech": note.pos,
                    "Gender": gender,
                    "Number": number,
                },
                "options": {"allowDuplicate": False},
                "tags": [],
            },
        )

    def add_notes(self, selected_note_indices):
        for selected_note_index in selected_note_indices:
            note = self.session.notes[selected_note_index]
            self.add_note(
                note,
            )
