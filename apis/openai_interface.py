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

    def get_french_and_english_strings_system_prompt(self):
        return """
            You will receive a string in French. Return a JSON object with a "french" field, 
            containing a cleaned up version of the input string (correct misspellings, accents, 
            etc.), and an "english" field, containing the English translation of "french".

            Example:

            Input: Vous netes pas oblige, dit-il. Je le sais bien, mais je veux t'offrir un animal.
            Output: {
                "french": "Vous n'êtes pas obligé, dit-il. Je le sais bien, mais je veux t'offrir un animal.",
                "english": "You are not obliged, he said. I know, but I want to give you an animal."
            }
        """

    def get_french_and_english_strings(self, input):
        system_prompt = self.get_french_and_english_strings_system_prompt()
        response_str = self.call_api(system_prompt, input)
        response_obj = json.loads(response_str)
        return response_obj

    def confirm_tokens_system_prompt(self):
        return """
            You will receive a JSON request object formatted as follows:

            {
                "string": a French string,
                "tokens": an array of JSON objects representing the tokens in "string" in exact order
            }

            Your job is to return a JSON array with a response object for each "token" in "tokens". 
            Each "token" will be formatted as follows:

            {
                "representation": the exact way the token is represented in "string",
                "note_front": a "generalized" form of "representation" (may be the original "representation" or its lemma),
                "pos": the part of speech "token" is functioning as in the string
            }

            Analyze each "token" in the context of "string". If "token" is functioning as a verb, 
            and "pos" is not ALREADY "verb", return the following:

            {
                "note_front": the infinitive form of the verb you have determined "token" to be,
                "english": the English translation of "note_front"
            }

            Otherwise, if "pos" is already "verb", or if "token" is functioning as any other part 
            of speech, return the following:

            {
                "english": the English translation of "note_front" from the request
            }

            English verb translations should usually be preceded by "to" (e.g. "to be", "to have").

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
                    "english": "of" // translating "de" that comes from "d'" in "d'avaler"
                },
                {
                    "english": "to swallow" // translating "avaler" that comes from "avaler" in "d'avaler"
                }
                ... // other "token"s
            ]
            Incorrect output: [
                ..., // other "token"s
                {
                    "note_front": "avaler",
                    "english": "to swallow", // Translating "avaler" that comes from "avaler" in "d'avaler". Should instead translate "de".
                    "pos": "verb"
                },
                {
                    "english": "to swallow" // Translating "avaler" that comes from "avaler" in "d'avaler" again. Technically correct in this position, but redundant because of the mistake made above.
                }
                ... // other "token"s
            ]
        """

    def confirm_tokens(self, input):
        system_prompt = self.confirm_tokens_system_prompt()
        response_str = self.call_api(system_prompt, input)
        response_obj = json.loads(response_str)
        return response_obj

    def get_note_details_system_prompt(self):
        return """
            You will receive a JSON object in the following format:

            {
                "string": a French string with a single component token bracketed
                "french": a "generalized" form of the bracketed token (may be a lemma, an infinitive form of the verb, the full form if the token is a fragment, etc.)
                "pos": the part of speech that the token is functioning as in the string
            }

            Your job is to analyze the bracketed bracketed token in the context of the string. If 
            the bracketed token is function as a verb in the string, and the "pos" field is not 
            ALREADY "verb", return the following:

            {
                "french": the infinitive form of the verb you have determined the token to be
                "english": the English translation of "french"
                "pos": "verb"
            }

            Otherwise, if the token is already correctly labeled as "verb", or the token is 
            functioning as any other part of speech, simply return the following:

            {
                "english": the English translation of "french" from the input object
            }

            In both cases, English translations of verbs should usually be preceded by "to" (e.g.
            "to be", "to have", "to go", etc.).

            With contractions, pay careful attention to which token within the contraction is
            bracketed. For example, if the input is this:

            Examples:

            Input: {
                "string": On a le temps [d']avaler quelque chose avant le départ du train, dit Hagrid.
                "french": "de",
                "pos": "preposition"
            }
            Correct output: {
                "english": "of" // translating the French "de" that comes from "d'" in "d'avaler"
            }
            Incorrect output: {
                "french": "avaler",
                "english": "to swallow", // translating the non-bracketed "avaler" portion of the contraction
                "pos": "verb"
            }

            Input: {
                "string": Je [m']appelle Jean.
                "french": "me",
                "pos": "pronoun"
            }
            Correct output: {
                "english": "myself" // translating the French "me" that comes from "m'" in "m'appelle"
            }
            Incorrect output: {
                "french": "appeler",
                "english": "to call", // translating the non-bracketed "appeler" portion of the contraction
                "pos": "verb"
            }
        """

    def get_note_details(self, input):
        system_prompt = self.get_note_details_system_prompt()
        response_str = self.call_api(system_prompt, input)
        response_obj = json.loads(response_str)
        return response_obj
