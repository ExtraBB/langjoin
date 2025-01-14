from langjoin.epub import transform_epub
from langjoin.transformers.transform_local import transform_text as transform_text_local
from langjoin.transformers.transform_llm import transform_text as transform_text_llm
from langjoin.transformers.transform_mock import transform_text as transform_text_mock

def main() -> int:
    transformer = lambda text: transform_text_llm(text, "pt", ["verb", "noun", "adjective", "adverb", "pronoun"], 0.5)
    transform_epub("static/epub/monkey.epub", 0, transformer)
    return 0