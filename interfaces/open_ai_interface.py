import json
import os

import openai
from dotenv import load_dotenv


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
        system_prompt = """
            You will receive a string in French in which one or more lexical tokens are bound by 
            square brackets. For each bracketed token, determine the part of speech that token is
            playing in the string, then return an array of corresponding JSON object.

            Choose from the following parts of speech:

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

            Return a JSON object in the following format for parts of speech NOUN, PROPN, PRON, ADV, 
            ADJ, ADP:

            {
                "token": The token exactly as it appears in the string,
                "pos": Token's part of speech abbreviation,
                "source": Token, but lowercase unless a proper noun,
                "target": English translation of "source",
                "gender": "MASC" or "FEM" (e.g. "sa" -> "FEM", "son" -> "MASC"). null if not 
                        applicable.
                "number": "SING" or "PLUR" (e.g. "papier" -> "SING", "papiers" -> "PLUR"). null if 
                        not applicable.
            }

            Return a JSON object in the following format for all other parts of speech:

            {
                "token": The token between brackets exactly as it appears in the string,
                "pos": Token's part of speech abbreviation,
                "source": Token's lemma,
                "target": English translation of the token's lemma, preceded by "to" if a verb (e.g.
                        "voir" -> "to see")
            }
        """

        bracketed_text = text.get_marked_text()

        response_str = self.call_api(system_prompt, bracketed_text)
        response_obj = json.loads(response_str)

        for item in response_obj:
            print(item)
