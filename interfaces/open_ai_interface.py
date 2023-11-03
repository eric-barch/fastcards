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
        print(systemPrompt)
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
            # You will receive a JSON object with properties "terms" and "string". "terms" is an array
            # of selected lexical tokens in the order they appear in "string". "string" is the source 
            # text of "terms", with each "term" enclosed in square brackets to help you match them up.
            
            # Return an array of JSON objects with details for each "term". Your response array must 
            # have EXACTLY as many items as there are "terms" in the request. If there are duplicate 
            # "terms" in the request, return duplicate items in your response. NEVER return a JSON 
            # object for a "term" that is NOT included in "terms" and is NOT bracketed in "string".

            # Classify each "term" as one of the following parts of speech: ADJ, ADP, ADV, AUX, CONJ, 
            # CCONJ, DET, INTJ, NOUN, NUM, PART, PRON, PROPN, PUNCT, SCONJ, SYM, VERB, X, SPACE

            # Return the following JSON object for "terms" that are parts of speech NOUN, PROPN, PRON, 
            # ADJ, DET:

            # {{
            #     "token": Token exactly as it appears in the string,
            #     "pos": Abbreviation for the part of speech that token is playing in the context
            #             of "string",
            #     "source": Almost always the same as token. Always the same inflection. Lowercase 
            #             unless a proper noun. If the word is truncated in the string (e.g. as part 
            #             of a contraction), un-truncate it.
            #     "target": {target_language} translation of source,
            #     "gender": "MASC" or "FEM" (e.g. "sa" -> "FEM", "son" -> "MASC"). null if not 
            #             applicable.
            #     "number": "SING" or "PLUR" (e.g. "papier" -> "SING", "papiers" -> "PLUR"). null if 
            #             not applicable.
            # }}

            # Return the following JSON object for "terms" that are all other parts of speech:

            # {{
            #     "token": Token exactly as it appears in the string,
            #     "pos": token's part of speech abbreviation,
            #     "source": token's lemma,
            #     "target": {target_language} translation of token's lemma, preceded by "to" if a verb
            #             (e.g. "voir" -> "to see")
            # }}

            Example requests and desired responses:

            request: {{
                "terms": ["ne", "sais", "pas", "dit"], 
                "string": "Je [ne] [sais] [pas], [dit] Harry."
            }}
            response: [
                {{
                    "token": "ne",
                    "pos": "ADV",
                    "source": "ne",
                    "target": "not"
                }},
                {{
                    "token": "sais",
                    "pos": "VERB",
                    "source": "savoir",
                    "target": "to know"
                }},
                {{
                    "token": "pas",
                    "pos": "ADV",
                    "source": "pas",
                    "target": "not"
                }},
                {{
                    "token": "dit",
                    "pos": "VERB",
                    "source": "dire",
                    "target": "to say"
                }}
            ]

            request: {{
                "terms": [
                    "Non",
                    "emm\u00e8ne",
                    "\u00e0",
                    "l'",
                    "h\u00f4pital"
                ],
                "string": "[Non], j'[emm\u00e8ne] Dudley [\u00e0] [l'][h\u00f4pital]."
            }}
            response: [
                {{
                    "token": "Non",
                    "pos": "INTJ",
                    "source": "non",
                    "target": "no",
                }},
                {{
                    "token": "emmène",
                    "pos": "VERB",
                    "source": "emmener",
                    "target": "to take",
                }},
                {{
                    "token": "à",
                    "pos": "ADP",
                    "source": "à",
                    "target": "to",
                }},
                {{
                    "token": "l'",
                    "pos": "DET",
                    "source": "le",
                    "target": "the",
                    "gender": "MASC",
                    "number": "SING",
                }},
                {{
                    "token": "hôpital",
                    "pos": "NOUN",
                    "source": "hôpital",
                    "target": "hospital",
                    "gender": "MASC",
                    "number": "SING",
                }}
            ]
        """

        marked_tokens = text.get_marked_tokens()
        marked_string = text.get_marked_string()

        request = {
            "terms": [token.text for token in marked_tokens],
            "string": marked_string,
        }

        print(f"OpenAI request: {json.dumps(request, indent=4)}")

        response = self.call_api(system_prompt, marked_string)

        print(response)

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
