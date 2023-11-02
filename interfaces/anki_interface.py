import json
import urllib.request
from models.note import Note, InflectedNote


class AnkiInterface:
    def __init__(self):
        self.read_deck = None
        self.write_deck = None

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

    def get_all_decks(self):
        return self.call_api("deckNames")

    def set_decks(self, read_deck, write_deck):
        self.read_deck = read_deck
        self.write_deck = write_deck

    def find_existing_notes(self, text):
        for token in text.tokens:
            query = f'deck:"{self.read_deck}" source:"{token.text}" or source:"{token.lemma}"'
            notes = self.call_api("findNotes", query=query)
            if notes:
                notes_info = self.call_api("notesInfo", notes=notes)
                for note_info in notes_info:
                    id = note_info.get("noteId")

                    fields = note_info.get("fields")

                    pos = fields.get("pos").get("value")
                    source = fields.get("source").get("value")
                    target = fields.get("target").get("value")

                    note = None

                    if "gender" in fields:
                        gender = fields.get("gender").get("value")
                        number = fields.get("number").get("value")
                        note = InflectedNote(pos, source, target, gender, number, id)
                    else:
                        note = Note(pos, source, target, id)

                    token.add_note(note)

    def find_notes(self, text):
        query = f'deck:"{self.read_deck}" source:"{text}"'
        response = self.call_api("findNotes", query=query)
        if response:
            notes_info = self.call_api("notesInfo", notes=response)
            for note_info in notes_info:
                id = note_info.get("noteId")
                fields = note_info.get("fields")
                source = fields.get("source").get("value")
                target = fields.get("target").get("value")
                existing_note = Note(id, source, target)
                print(existing_note)
