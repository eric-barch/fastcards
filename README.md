# Fastcards

Automatically generate Anki flashcards as you read a foreign language.

## Use Case

[Anki](https://apps.ankiweb.net/) is a free, open-source flashcard application. Its use of [spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition) makes it good for building and retaining a vocabulary in a new language. But making flashcards can be time-consuming and borderline distracting when you're trying to work through a foreign text. You may find yourself creating cards only for "major" parts of speech like nouns, verbs, and adjectives, leaving you with a weak understanding of articles, determiners, and other "minor" parts of speech. Fastcards accepts text input as you read, then automatically tells you which terms already have cards and allows you to generate flashcards for ones that don't.

## Dependencies

- The [OpenAI API](https://platform.openai.com/docs/models) is used to translate and tag terms. You will need to supply your own OpenAI API key.
- spaCy's [natural language processing models](https://spacy.io/models) (in this repo, [French](https://spacy.io/models/fr#fr_dep_news_trf)) are used to tokenize input. They are free and run locally.
- The [AnkiConnect](https://github.com/FooSoft/anki-connect) Anki plugin is used to interface with Anki's underlying database.

## Install and Setup

1. Clone this repo.
2. Create and activate a Python virtual environment (optional, but good practice).
3. Run the setup script: `python setup.py`
4. If you don't already have Anki on your machine, [install it](https://apps.ankiweb.net/).
5. [Download the AnkiConnect add-on](https://ankiweb.net/shared/info/2055492159).
6. [Set up an OpenAI API key](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key). Set the `OPENAI_API_KEY` variable in the `.env` file that was created by `setup.py`.

## How to Use

1. Activate your Python virtual environment if applicable.
2. Run `python main.py`.
3. Choose a read and write Anki deck. The read deck will be used to check for existing flashcards, and new flashcards will be saved in the write deck.
4. As you read, type unknown words or sentences into the prompt. Strings will be broken up into their component tokens, translated, and you will be given the option to save them as new flashcards.
5. That's it! Use all the time you saved to study flashcards instead of making them!
