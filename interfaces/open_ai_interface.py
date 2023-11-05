import json
import os

import openai
from dotenv import load_dotenv
from global_variables import source_language
from models.note import Note


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
            You will receive a string in {source_language}. Return an array of JSON objects for 
            each of the bracketed tokens. Each JSON object should include fields "token", "pos",
            "source", "target", "gender", and "number".

            Example full request and desired response:

            request: "Je dois prendre le train à la gare de King's Cross à [onze] [heures]."
            response: [
                {{
                    "token": "onze",
                    "pos": "NUM",
                    "source": "onze",
                    "target": "eleven",
                    "gender": null,
                    "number": null
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

            Example request ITEMS and their desired response ITEM. These are the components that 
            will make up your full response array, provided as additional training material. 
            
            If the token is a VERB, "source" and "target" should both be in their infinitive form, 
            e.g. "réveiller" and "to wake up". 

            ENSURE THAT YOUR RESPONSE ARRAY ALWAYS CONTAINS EXACTLY THE SAME NUMBER OF ITEMS AS
            THERE ARE BRACKETED TOKENS IN THE REQUEST STRING.

            request item: "pleine"
            response item: {{
                "token": "pleine",
                "pos": "ADJ",
                "source": "pleine",
                "target": "full",
                "gender": "FEM",
                "number": "SING"
            }}

            request item: "regardant"
            response item: {{
                "token": "regardant",
                "pos": "VERB",
                "source": "regarder",
                "target": "to look",
                "gender": null,
                "number": null
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
            response item: {{ // note: inferred from string context
                "token": "C'",
                "pos": "PRON",
                "source": "ce",
                "target": "it",
                "gender": "MASC",
                "number": "SING"
            }}

            request item: "est"
            response item: {{
                "token": "est",
                "pos": "VERB",
                "source": "\u00eatre",
                "target": "to be",
                "gender": null,
                "number": null
            }}

            request item: "Tous"
            response item: {{
                "token": "Tous",
                "pos": "ADJ",
                "source": "tous",
                "target": "all",
                "gender": "MASC",
                "number": "PLUR"
            }}

            request item: "essayant"
            response item: {{
                "token": "essayant",
                "pos": "VERB",
                "source": "essayer",
                "target": "to try",
                "gender": null,
                "number": null
            }}

            request item: "au"
            response item: {{
                "token": "au",
                "pos": "PREP",
                "source": "au",
                "target": "to the",
                "gender": "MASC",
                "number": "SING"
            }}

            request item: "Inutile"
            response item: {{
                "token": "Inutile",
                "pos": "ADJ",
                "source": "inutile",
                "target": "useless",
                "gender": null,
                "number": "SING"
            }},

            request item: "scolaires"
            response item: {{
                "token": "scolaires",
                "pos": "ADJ",
                "source": "scolaires",
                "target": "scholastic",
                "gender": null,
                "number": "PLUR"
            }}
        """

        print(f"OpenAI request: {text.get_marked_string()}")

        request = text.get_marked_string()
        response = json.loads(self.call_api(system_prompt, request))

        # for debugging
        # print(f"OpenAI response: {json.dumps(response, indent=4)}")

        marked_tokens = text.get_marked_tokens()

        if len(response) != len(marked_tokens):
            print(
                f"\n\033[31mWARN:\033[0m received different number of responses than requests sent"
            )

        for i, item in enumerate(response):
            pos = item.get("pos")
            source = item.get("source")
            target = item.get("target")
            gender = item.get("gender")
            number = item.get("number")

            note = Note(pos, source, target, None, gender, number)

            marked_tokens[i].add_note(note)
