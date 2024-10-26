import random
from typing import Callable, List
import spacy
from translate import Translator

nlp = spacy.load("en_core_web_sm")

def translate_text(text: str, lang: str) -> str:
    translator = Translator(to_lang=lang)
    return translator.translate(text)

def transform_text(text: str, lang: str, word_types: List[str], strength: float) -> str:
    doc = nlp(text)
    
    new_text = ""

    # Iterate through tokens and apply translation based on strength
    for token in doc:
        if spacy.glossary.explain(token.pos_) in word_types and random.random() < strength:
            translated = translate_text(token.text_with_ws, lang)
            new_text += translated + " "
        else:
            new_text += token.text_with_ws
    
    return new_text