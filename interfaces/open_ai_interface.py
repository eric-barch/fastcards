import json
import os

import openai
from dotenv import load_dotenv
from global_variables import source_language
from models.note import Note

GPT_MODEL = "gpt-3.5-turbo-1106"


class OpenAiInterface:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def call_api(self, systemPrompt: str, string: str):
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": systemPrompt},
                {
                    "role": "user",
                    "content": string,
                },
            ],
        )

        if response.choices[0].finish_reason != "length":
            return response.choices[0].message.content

        raise Exception("Response terminated due to length.")

    def look_up_tokens(self, text):
        system_prompt = f"""
            For a given string in {source_language.capitalize()}, return an array of JSON objects, 
            one for each bracketed token. Include fields: "token", "pos", "source", "target", 
            "gender", and "number". 
            
            For "pos", choose from the following: ADJ, ADP, ADV, AUX, CONJ, CCONJ, DET, INTJ, NOUN, 
            NUM, PART, PRON, PROPN, PUNCT, SCONJ, SYM, VERB, X
            
            If the token is a VERB, "source" and "target" should be in their infinitive form. 
            
            IMPORTANT: Your response must always be an ARRAY, even if their is only one JSON object
            in it. Your response array MUST have the same number of items as there are bracketed 
            tokens in the request. 
            
            Use the following examples as guidance to craft your response.
           
            Generic example:

            Response: {{
                "token": token text, always EXACTLY how it appears inside brackets in the string,
                "pos": part of speech abbreviation,
                "source": the {source_language.capitalize()} word, always lowercase unless PROPN
                "target": English translation of source, always lowercase unless PROPN
                "gender": "MASC", "FEM", or null,
                "number": "SING", "PLUR", or null,
            }}
           
            Other examples:

            Numerical Value:

            Request: "[onze]"
            Response: {{
                "token": "onze",
                "pos": "NUM",
                "source": "onze",
                "target": "eleven",
                "gender": null,
                "number": null
            }}

            Noun:

            Request: "[heures]"
            Response: {{
                "token": "heures",
                "pos": "NOUN",
                "source": "heures",
                "target": "hours",
                "gender": "FEM", // NOUNs almost always have gender
                "number": "PLUR" // NOUNs almost always have number
            }}

            Adjective:

            Request: "[pleine]"
            Response: {{
                "token": "pleine",
                "pos": "ADJ",
                "source": "pleine",
                "target": "full",
                "gender": "FEM", // ADJs almost always have gender
                "number": "SING" // ADJs almost always have number
            }}
            
            Verb in non-infinitive form:

            Request: "[regardant]"
            Response: {{
                "token": "regardant", // exactly as appears inside brackets
                "pos": "VERB",
                "source": "regarder", // infinitive
                "target": "to look", // infinitive
                "gender": null,
                "number": null
            }}

            Short Form/Abbreviated Token:

            Request: "[C']"
            Response: {{
                "token": "C'", // exactly as appears in string
                "pos": "PRON",
                "source": "ce", // unabbreviated form inferred from string context
                "target": "it",
                "gender": "MASC",
                "number": "SING"
            }}

            Part of Contraction Tokens:

            Request: "[Ferme]-la"
            Response: {{
                "token": "Ferme", // "-la" ignored because not inside brackets
                "pos": "VERB",
                "source": "fermer",
                "target": "to close",
                "gender": null,
                "number": null
            }}

            Request: "s'[éloigna]"
            Response: {{
                "token": "éloigna", // "s'" ignored because not inside brackets
                "pos": "VERB",
                "source": "éloigner",
                "target": "to move away",
                "gender": null,
                "number": null
            }}
        """

        request = text.get_marked_string()

        print(f"OpenAI request: {request}")

        response = json.loads(self.call_api(system_prompt, request))

        print(f"OpenAI response: {json.dumps(response, indent=4)}")

        if not isinstance(response, list):
            response = [response]

        marked_tokens = text.get_marked_tokens()

        if len(response) != len(marked_tokens):
            print(
                f"\n\033[31mWARN:\033[0m received different number of responses than requests sent"
            )

        for marked_token in marked_tokens:
            response_match = None

            for item in response:
                if item.get("token") == marked_token.text.string:
                    response_match = item
                    break

            # TODO: Ask again for items that were missed. Can pretty much just do it by running the
            # above again.
            if response_match is None:
                print(
                    f"\033[31mWARN:\033[0m skipping {marked_token.text.string} "
                    f"(did not find matching response item)"
                )
                continue

            pos = item.get("pos")
            source = item.get("source")
            target = item.get("target")
            gender = item.get("gender")
            number = item.get("number")

            note = Note(pos, source, target, None, gender, number)

            marked_token.add_note(note)
