from typing import Callable, List
import spacy
nlp = spacy.load("en_core_web_sm")

def get_sentences(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

def get_noun_chunks(sentence: str):
    doc = nlp(sentence)
    return [nc.text for nc in doc.noun_chunks]

def replace_noun_chunks(sentence: str, replace_func: Callable[[str], str]) -> str:
    doc = nlp(sentence)
    new_sentence = ""
    
    last_token_index_added = -1
    for chunk in doc.noun_chunks:
        # Add tokens before the chunk
        for i in range(last_token_index_added + 1, chunk.start):
            new_sentence += doc[i].text_with_ws
            
        # Add the replaced noun chunk
        new_sentence += replace_func(chunk.text)
        
        # Add any whitespace after the chunk
        if chunk.end < len(doc) and doc[chunk.end - 1].whitespace_:
            new_sentence += " "
            
        last_token_index_added = chunk.end - 1
    
    # Add remaining tokens after the last chunk
    for i in range(last_token_index_added + 1, len(doc)):
        new_sentence += doc[i].text_with_ws
        
    return new_sentence
        
    