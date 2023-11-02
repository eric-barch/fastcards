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
            You will receive a string in {source_language} with one or more tokens enclosed in 
            square brackets. Return an array of JSON objects with token details. Your response array 
            must have exactly as many items as there are bracketed tokens in the request.

            Classify each token as one of the following parts of speech:

            adjective (ADJ)
            adposition (ADP)
            adverb (ADV)
            auxiliary verb (AUX)
            coordinating conjunction (CONJ)
            coordinating conjunction (CCONJ)
            determiner (DET)
            interjection (INTJ)
            noun (NOUN)
            numeral (NUM)
            particle (PART)
            pronoun (PRON)
            proper noun (PROPN)
            punctuation (PUNCT)
            subordinating conjunction (SCONJ)
            symbol (SYM)
            verb (VERB)
            other (X)
            space (SPACE)

            Return the following JSON object for parts of speech NOUN, PROPN, PRON, ADV, ADJ, ADP:

            {{
                "token": The token exactly as it appears in the string,
                "pos": token's part of speech abbreviation,
                "source": Almost always the same as token. Lowercase unless a proper noun. If the 
                        word is truncated in the request string (e.g. as part of a contraction), the
                        full word.
                "target": {target_language} translation of source,
                "gender": "MASC" or "FEM" (e.g. "sa" -> "FEM", "son" -> "MASC"). null if not 
                        applicable.
                "number": "SING" or "PLUR" (e.g. "papier" -> "SING", "papiers" -> "PLUR"). null if 
                        not applicable.
            }}

            Return the following JSON object for all other parts of speech:

            {{
                "token": The token exactly as it appears in the string,
                "pos": token's part of speech abbreviation,
                "source": token's lemma,
                "target": {target_language} translation of token's lemma, preceded by "to" if a verb
                        (e.g. "voir" -> "to see")
            }}
        """

        marked_string = text.get_marked_string()

        print(f"OpenAI request: {marked_string}")

        response = self.call_api(system_prompt, marked_string)
        deserialized_response = json.loads(response)

        print(f"OpenAI response: {json.dumps(deserialized_response, indent=4)}")

        marked_tokens = text.get_marked_tokens()

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
