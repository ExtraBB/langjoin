from typing import Callable
import epubfile

def transform_epub(path: str, max_paragraphs: int, transformer: Callable[[str], str]):
    book = epubfile.Epub(path)
    paragraphs_transformed = 0
    
    for text_id in book.get_texts():
        soup = book.read_file(text_id, soup=True)
        for p in soup.find_all("p"):
            if len(p.text) > 100:
                new_text = transformer(p.text)
                print("Replacing:\n\n" + p.text + "\n\nWith:\n\n" + new_text)
                p.string.replace_with(new_text)
                paragraphs_transformed += 1
                if paragraphs_transformed >= max_paragraphs:
                    return
        book.write_file(text_id, soup)