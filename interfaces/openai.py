import json
import os

import openai
from dotenv import load_dotenv


class OpenAiInterface:
    def __init__(self, session):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.session = session
        session.openai_interface = self

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

    def get_source_and_target_strings_system_prompt(self):
        return """
            You will receive a string in Source. Return a JSON object with a "source" field, 
            containing a cleaned up version of the input string (correct misspellings, accents, 
            etc.), and an "target" field, containing the Target translation of "source".

            Example:

            Input: Vous netes pas oblige, dit-il. Je le sais bien, mais je veux t'offrir un animal.
            Output: {
                "source": "Vous n'êtes pas obligé, dit-il. Je le sais bien, mais je veux t'offrir un animal.",
                "target": "You are not obliged, he said. I know, but I want to give you an animal."
            }
        """

    def get_source_and_target_strings(self, input):
        system_prompt = self.get_source_and_target_strings_system_prompt()
        response_str = self.call_api(system_prompt, input)
        response_obj = json.loads(response_str)
        return response_obj

    def confirm_tokens_system_prompt(self):
        return """
            You will receive a JSON object formatted as follows:

            {
                "string": a Source string,
                "tokens": an array of JSON objects representing the tokens in "string" in exact order
            }
 
            Each "token" within "tokens" will be formatted as follows:

            {
                "representation": the exact way the token appears in "string",
                "note_front": a "generalized" form of "representation" (may be the original "representation" or its lemma),
                "pos": the part of speech "token" is functioning as in the string
            }

            Your job is to confirm that the "note_front" and "pos" fields are correct and provide 
            an Target translation. Analyze each token in the context of the full string and return 
            an array of JSON objects formatted as follows for each "token":

            {
                "note_front": string,
                "note_back": string,
                "pos": string,
            }

            "note_front":
                -   Should usually be the same as "token"'s "representation" unless:
                    -   "token" is part of a contraction (usually ending in "'"), or is an inverted 
                        subject pronoun (usually starting with "-"). In this case, "note_front" 
                        should be "token"'s lemma.
                    -   "token" is functioning as a verb in the original string. In this case, 
                        "note_front" should be the infinitive form of "token".
                -   If "token" is a proper noun in the original string, "note_front" should be
                    capitalized. Otherwise, "note_front" should be lowercase.

            "note_back":
                -   Target verb translations should usually be preceded by "to" (e.g. "to be",
                    "to have"). 
                -   Case should match the case of "note_front".

            "pos":
                -   Make sure the token is actually functioning as the "pos" in the request object.
                    If it is not, return the correct "pos".
                -   Choose from the following options:
                        "adjective",
                        "adposition",
                        "adverb",
                        "auxiliary",
                        "conjunction",
                        "coord conj",
                        "determiner",
                        "interjection",
                        "noun",
                        "numeral",
                        "particle",
                        "pronoun",
                        "proper noun",
                        "punctuation",
                        "subord conj",
                        "symbol",
                        "verb",
                        "other",
                        "space"
                
            With contractions, pay careful attention to which token within the contraction is
            referenced. For example:

            Input: {
                "string": "On a le temps d'avaler quelque chose avant le départ du train.",
                "token_data": [
                    ..., // other "token"s
                    {
                        "representation": "d'".
                        "note_front": "de",
                        "pos": "preposition"
                    },
                    {
                        "representation": "avaler",
                        "note_front": "avaler",
                        "pos": "verb"
                    }
                    ... // other "token"s
                ]
            }
            Correct output: [
                ..., // other "token"s
                {
                    "note_front": "de", // from "d'" in "d'avaler"
                    "note_back": "of",
                    "pos": "preposition"
                },
                {
                    "note_front": "avaler", // from "avaler" in "d'avaler"
                    "note_back": "to swallow",
                    "pos": "verb"
                }
                ... // other "token"s
            ]
            Incorrect output: [
                ..., // other "token"s
                {
                    "note_front": "avaler", // from "avaler" in "d'avaler" - should be "de"
                    "note_back": "to swallow",
                    "pos": "verb"
                },
                {
                    "note_front": "avaler", // from "avaler" in "d'avaler" again - technically correct in this position, but redundant because of mistake above
                    "note_back": "to swallow",
                    "pos": "verb"
                }
                ... // other "token"s
            ]
        """

    def confirm_tokens(self, input):
        system_prompt = self.confirm_tokens_system_prompt()
        response_str = self.call_api(system_prompt, input)
        response_obj = json.loads(response_str)
        return response_obj
