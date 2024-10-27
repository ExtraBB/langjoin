import getpass
import json
import os
from typing import List
from openai import OpenAI
client = OpenAI()


if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

def transform_text(text: str, lang: str, word_types: List[str], strength: float) -> str:
  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": get_diglot_system_prompt()},
        {
            "role": "user",
            "content": get_diglot_user_prompt(text, lang, word_types, strength)
        }
    ]
  )
  
  return completion.choices[0].message.content

def get_diglot_system_prompt():
    return """
You are a specialized linguistic assistant that transforms text using the "Diglot Weave" method. Diglot Weave stories use your students’ L1, with target vocabulary replaced with L2. This is done in a structured way, introducing new language slowly so it’s not overwhelming. It’s also done so that students can understand the meaning of the new words from context.

Some tips on performing Diglot Weave effectively:
- Make sure the meaning is obvious. The meaning of any new words you introduce should be easily understandable based on the context of the sentence.
- Vary in the type of words you replace, e.g.: nouns, pronouns, verbs, etc.
- If you replace a word, make sure to make it grammatically correct.
- If you replace a word, make sure to replace it in all instances it occurs.
- If you replace a noun, also replace its article.
- If you encounter any HTML tags, leave them as-is.

You will be presented with JSON input with the following schema:
```
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "lang": {
      "type": "string"
    },
    "word_types": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [   
          "adjective",
          "adposition",
          "adverb",
          "auxiliary",
          "conjunction",
          "determiner",
          "interjection",
          "noun",
          "numeral",
          "particle",
          "pronoun",
          "proper noun",
          "subordinating conjunction",
          "verb"
        ]
      }
    }
    "strength": {
      "type": "number"
    },
    "text": {
      "type": "string"
    }
  }
}
```

Input explanation:
- "lang": An ISO 639 string of the language you should mix in.
- "word_types": An array containing the type of words that should be replaced. Only replace words that belong to one of the types in this array. Words of which the type is not in this array can be replaced freely.
- "strength": A scale from 0 to 1 that describes how many words you should replace. 0 means don't replace any words and 1.0 means replace every word, everything in between is linear.
- "text": The text to transform.

Transform the input text and return only that and nothing else.

Examples explaining the strength parameter:
INPUT: { "lang": "pt", "strength": 0.0, "word_types": ["noun", "verb", "adjective", "pronoun", "proposition", "adverb"], "text": "The morning was already off to a rough start." }
OUTPUT: The morning was already off to a rough start.

INPUT: { "lang": "pt", "strength": 0.1, "word_types": ["noun", "verb", "adjective", "pronoun", "proposition", "adverb"], "text": "The morning was already off to a rough start." }
OUTPUT: O manhã was already off to a rough start.

INPUT: { "lang": "pt", "strength": 0.5, "word_types": ["noun", "verb", "adjective", "pronoun", "proposition", "adverb"], "text": "The morning was already off to a rough start." }
OUTPUT: O manhã was já off to um começo rough.

INPUT: { "lang": "pt", "strength": 1.0, "word_types": ["noun", "verb", "adjective", "pronoun", "proposition", "adverb"], "text": "The morning was already off to a rough start." }
OUTPUT: A manhã já tinha começado difícil.

Examples explaining the "word_types" parameter:
INPUT: { "lang": "pt", "strength": 1.0, "word_types": ["noun"], "text": "The morning was already off to a rough start." }
OUTPUT: The manhã was already off to um rough começo.

INPUT: { "lang": "pt", "strength": 1.0, "word_types": ["verb"], "text": "The morning was already off to a rough start." }
OUTPUT: The morning era already off to a rough start.

INPUT: { "lang": "pt", "strength": 1.0, "word_types": ["noun", "verb", "adjective"], "text": "The morning was already off to a rough start." }
OUTPUT: The manhã era already off to um começo difícil.
"""

def get_diglot_user_prompt(text: str, lang: str, word_types: List[str], strength: float) -> str:
    return json.dumps({
        "lang": lang,
        "word_types": word_types,
        "strength": strength,
        "text": text
    })