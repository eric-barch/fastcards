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

    def get_source_and_target_system_prompt(self):
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

    def get_source_and_target(self, text):
        system_prompt = self.get_source_and_target_system_prompt()
        response_str = self.call_api(system_prompt, text)
        response_obj = json.loads(response_str)

        source = response_obj["source"]
        target = response_obj["target"]

        return source, target

    def get_tokens_system_prompt(self):
        return """
            You will receive a JSON object formatted as follows:

            {
                "string": a string in French,
                "tokens": a JSON array of the tokens in "string" in exact order
            }
 
            Each "token" object within "tokens" will be formatted as follows:

            {
                "representation": the exact way the token appears in "string",
                "source": the original "representation" or its lemma,
                "pos": "token"'s part of speech,
                "gender": "token"'s gender, if any,
                "number": "token"'s number, if any,
            }

            Use this as a (possibly inaccurate) starting point to analyze each token in the context 
            of the string. Return an array of corrected JSON objects with an English translation as 
            below. There should always be exactly as many objects in your response array as there 
            were in the input "tokens" array.

            {
                "source": corrected "source",
                "target": English translation of crrected "source" (NOT "representation"),
                "pos": part of speech of corrected "source" (choose from below),
                "gender": gender of corrected "source", if any (choose from below),
                "number": number of corrected "source", if any (choose from below)
            }

            "pos" options:
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
            
            "gender" options:
                "masculine",
                "feminine",
                "neuter",
            
            "number" options:
                "singular",
                "plural"
            
            Below are some examples of an input string with the relevant token bracketed, and the 
            correct output object for that token.

            Input: Je [suis] un homme.
            Output: {
                "source": "être", // verb "source"s are always lemmas
                "target": "to be", // verb "target"s are always infinitives
                "pos": "verb",
                "gender": null,
                "number": null
            }

            Input: Je [m'][appelle] [Jean].
            Output 1: {
                "source": "me", // lemma of "m'" from "m'appelle"
                "target": "myself",
                "pos": "pronoun",
                "gender": null,
                "number": null
            }
            Output 2: {
                "source": "appeler", // lemma of "appelle" from "m'appelle"
                "target": "to call",
                "pos": "verb",
                "gender": null,
                "number": null
            }
            Output 3: {
                "source": "Jean", // proper nouns remain capitalized
                "target": "Jean",
                "pos": "proper noun",
                "gender": masculine,
                "number": singular
            }

            Input: [Bonjour], mon ami. Comment ça va?
            Output: {
                "source": "bonjour", // lowercase because not proper noun
                "target": "hello",
                "pos": "interjection",
                "gender": null,
                "number": null
            }
        """

    def get_tokens(self, request):
        system_prompt = self.get_tokens_system_prompt()
        response_str = self.call_api(system_prompt, json.dumps(request))
        response_obj = json.loads(response_str)
        return response_obj
