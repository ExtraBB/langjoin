import epubfile
import spacy

def load(path: str):
    book = epubfile.Epub(path)
    nlp = spacy.load("en_core_web_sm")
                
    for text_id in book.get_texts():
        soup = book.read_file(text_id, soup=True)
        for p in soup.find_all("p"):

            if (len(p.text) > 100):
                doc = nlp(p.text)
                sentences = [sent.text for sent in doc.sents]
                print(sentences)
                return