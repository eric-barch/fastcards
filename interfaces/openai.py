import json
import os

import openai
from dotenv import load_dotenv


class OpenAi:
    def __init__(self, session):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.session = session
        session.openai = self

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

    def get_text_source_and_target_system_prompt(self):
        return """
            You will receive a string in French (the source language). Return a JSON object with a 
            "source" field, containing a cleaned up version of the input string (correct 
            misspellings, accents, etc.), and an "target" field, containing the English (the target
            language) translation of "source".

            Example:

            Input: Vous netes pas oblige, dit-il. Je le sais bien, mais je veux t'offrir un animal.
            Output: {
                "source": "Vous n'êtes pas obligé, dit-il. Je le sais bien, mais je veux t'offrir un animal.",
                "target": "You are not obliged, he said. I know, but I want to give you an animal."
            }
        """

    def get_text_source_and_target(self, text):
        system_prompt = self.get_text_source_and_target_system_prompt()
        response_str = self.call_api(system_prompt, text)
        response_obj = json.loads(response_str)
        return response_obj

    def get_tokens_system_prompt(self):
        return """
            You will receive a JSON object formatted as follows:

            {
                "string": a string in French (the source language),
                "tokens": a JSON array of the tokens in "string" in exact order
            }
 
            Each "token" object within "tokens" will be formatted as follows:

            {
                "representation": the exact way the token appears in "string",
                "source": a "generalized" form of "representation" (may be the original "representation" or its lemma),
                "pos": the part of speech "token" is functioning as in the string,
                "gender": the token's gender, if any,
                "number": the token's number, if any,
            }

            Your job is to analyze each token in the context of the string and confirm that the 
            information in the object you receive is correct. You should also provide a translation 
            of "source" in English (the target language). Return an array of JSON objects in the
            following format for each object in the request array:

            {
                "source": corrected "source",
                "target": translation of corrected "source",
                "pos": corrected "pos",
                "gender": corrected "gender", if any,
                "number": corrected "number", if any,
            }

            Please note the following in your response:
            
            "source":
                -   Should usually be the same as "token"'s "representation" unless:
                    -   "token" is part of a contraction (usually ending in "'"), or is an inverted 
                        subject pronoun (usually starting with "-"). In this case, "source" 
                        should be "token"'s lemma.
                    -   "token" is functioning as a verb in the original string. In this case, 
                        "source" should be the infinitive form of "token".
                -   If the CORRECTED pos is not a proper noun, this field should be lowercase.

            "target":
                -   English verb translations should usually be preceded by "to" (e.g. "to be",
                    "to have").
                -   If the CORRECTED pos is not a proper noun, this field should be lowercase.

            "pos":
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
                
            "gender" and "number":
                -   Be sure to correct these fields to null if the concepts of gender and/or number
                    do not apply to "token".
                
            With contractions, pay careful attention to which token within the contraction is
            referenced. For example:

            Input: {
                "string": "On a le temps d'avaler quelque chose avant le départ du train.",
                "token_data": [
                    ..., // other "token"s
                    {
                        "representation": "d'".
                        "source": "de",
                        "pos": "preposition"
                        "gender": null,
                        "number": null,
                    },
                    {
                        "representation": "avaler",
                        "source": "avaler",
                        "pos": "verb",
                        "gender": null,
                        "number": null
                    }
                    ... // other "token"s
                ]
            }
            Correct output: [
                ..., // other "token"s
                {
                    "source": "de", // from "d'" in "d'avaler"
                    "target": "of",
                    "pos": "preposition",
                    "gender": null,
                    "number": null
                },
                {
                    "source": "avaler", // from "avaler" in "d'avaler"
                    "target": "to swallow",
                    "pos": "verb",
                    "gender": null,
                    "number": null
                }
                ... // other "token"s
            ]
            Incorrect output: [
                ..., // other "token"s
                {
                    "source": "avaler", // from "avaler" in "d'avaler" - should be "de"
                    "target": "to swallow",
                    "pos": "verb"
                    "gender": null,
                    "number": null
                },
                {
                    "source": "avaler", // from "avaler" in "d'avaler" again - technically correct in this position, but redundant because of mistake above
                    "target": "to swallow",
                    "pos": "verb",
                    "gender": null,
                    "number": null
                }
                ... // other "token"s
            ]
        """

    def get_tokens(self, request):
        system_prompt = self.get_tokens_system_prompt()
        response_str = self.call_api(system_prompt, json.dumps(request))
        response_obj = json.loads(response_str)
        return response_obj
