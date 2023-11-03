import json
import os

import openai
from dotenv import load_dotenv
from global_vars import source_language, target_language
from models.note import Note, InflectedNote


class OpenAiInterface:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def call_api(self, systemPrompt: str, string: str):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": systemPrompt},
                {
                    "role": "user",
                    "content": string,
                },
            ],
        )
        return response.choices[0].message.content

    def look_up_tokens(self, text):
        system_prompt = f"""
            You will receive a request in {source_language}. Return an array with {target_language}
            translation and other lexical information for the selected tokens. Below is an example
            of a full request and full response.

            request: {{
                "terms": [
                    "onze",
                    "heures"
                ],
                "string": "Je dois prendre le train \u00e0 la gare de King's Cross \u00e0 [onze] [heures]."
            }}
            response: [
                {{
                    "token": "onze",
                    "pos": "NUM",
                    "source": "onze",
                    "target": "eleven",
                }},
                {{
                    "token": "heures",
                    "pos": "NOUN",
                    "source": "heures",
                    "target": "hours",
                    "gender": "FEM",
                    "number": "PLUR"
                }}
            ]

            Below are some more examples of request ITEMS and their desired response ITEM. These are
            the components that will make up your full response array. They are provided as
            additional training material.

            request item: "regardant"
            response item: {{
                "token": "regardant",
                "pos": "VERB",
                "source": "regarder",
                "target": "to look"
            }}

            request item: "ronds"
            response item: {{
                "token": "ronds",
                "pos": "NOUN",
                "source": "ronds",
                "target": "round",
                "gender": "MASC",
                "number": "PLUR"
            }}

            request item: "C'"
            response item: {{
                "token": "C'",
                "pos": "PRON",
                "source": "ce",
                "target": "it",
                "gender": "MASC",
                "number": "SING", 
            }}

            request item: "est"
            response item: {{
                "token": "est",
                "pos": "VERB",
                "source": "\u00eatre",
                "target": "to be"
            }}

            request item: "tous"
            response item: {{
                "token": "tous",
                "pos": "ADJ",
                "source": "tous",
                "target": "all",
                "gender": "MASC",
                "number": "PLUR", 
            }}

            request item: "fous"
            response item: {{
                "token": "fous",
                "pos": "ADJ",
                "source": "fous",
                "target": "crazy",
                "gender": "MASC",
                "number": "PLUR", 
            }}
        """

        marked_tokens = text.get_marked_tokens()
        marked_string = text.get_marked_string()

        request = {
            "terms": [token.text for token in marked_tokens],
            "string": marked_string,
        }

        print(f"OpenAI request: {json.dumps(request, indent=4)}")

        response = self.call_api(system_prompt, marked_string)
        deserialized_response = json.loads(response)

        print(f"OpenAI response: {json.dumps(deserialized_response, indent=4)}")

        if len(marked_tokens) != len(deserialized_response):
            raise ValueError(
                "response has different number of items than marked_tokens"
            )

        for i, item in enumerate(deserialized_response):
            pos = item.get("pos")
            source = item.get("source")
            target = item.get("target")

            note = None

            if "gender" in item:
                gender = item.get("gender")
                number = item.get("number")
                note = InflectedNote(pos, source, target, gender, number)
            else:
                note = Note(pos, source, target)

            marked_tokens[i].add_note(note)
