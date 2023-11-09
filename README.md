# fastcards

For natural language learners. Read it once and remember.

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
6. Supply your own OpenAI API key. Store it in an environment variable or in a `.env` file.
7. Run the `main.py` script to start the program.

## How to Use

## Adapt for Other Languages
