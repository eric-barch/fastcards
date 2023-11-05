import json
import urllib.request

from models.note import Note


class AnkiInterface:
    def __init__(self):
        self.read_deck_name = None
        self.write_deck_name = None

    def call_api(self, action, **params):
        request = json.dumps({"action": action, "params": params, "version": 6}).encode(
            "utf-8"
        )
        response = json.load(
            urllib.request.urlopen(
                urllib.request.Request("http://localhost:8765", request)
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

    def set_deck_names(self, read_deck_name, write_deck_name):
        self.read_deck_name = read_deck_name
        self.write_deck_name = write_deck_name

    def find_existing_notes(self, text):
        for token in text.tokens:
            query = f'deck:"{self.read_deck_name}" ' + " or ".join(
                [
                    f'source:"{inflection_string}"'
                    for inflection_string in token.get_inflection_strings()
                ]
            )

            existing_note_ids = self.call_api("findNotes", query=query)

            if existing_note_ids:
                existing_note_infos = self.call_api(
                    "notesInfo", notes=existing_note_ids
                )

                for existing_note_info in existing_note_infos:
                    id = existing_note_info.get("noteId")

                    fields = existing_note_info.get("fields")

                    pos = fields.get("pos").get("value")
                    source = fields.get("source").get("value")
                    target = fields.get("target").get("value")
                    gender = fields.get("gender").get("value")
                    number = fields.get("number").get("value")

                    note = Note(pos, source, target, id, gender, number)

                    token.add_note(note)

    def add_notes(self, text):
        for token in text.tokens:
            for note in token.get_notes():
                if note.will_add:
                    anki_note = {
                        "deckName": self.write_deck_name,
                        "modelName": "french-term",
                        "fields": {
                            "source": note.source,
                            "target": note.target,
                            "pos": note.pos,
                            "gender": note.gender if note.gender else "NONE",
                            "number": note.number if note.number else "NONE",
                        },
                        "options": {
                            "allowDuplicate": False,
                            "duplicateScope": self.read_deck_name,
                        },
                    }

                    try:
                        self.call_api("addNote", note=anki_note)
                    except:
                        print(f"Skipped creating note for {note.source} (duplicate)")
                        continue
