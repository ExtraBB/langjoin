import epubfile

def load(path: str):
    book = epubfile.Epub(path)
                
    for text_id in book.get_texts():
        soup = book.read_file(text_id, soup=True)
        # for p in soup.find_all("p"):

        #     if (len(p.text) > 100):
        #         doc = nlp(p.text)
        #         sentences = [sent.text for sent in doc.sents]
        #         print(sentences)
        #         returns