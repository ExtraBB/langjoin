from pathlib import Path
from typing import Callable
from bs4 import BeautifulSoup
import epubfile

def transform_epub(path: str, max_paragraphs: int, transformer: Callable[[str], str]):
    """
    Transform paragraphs in an EPUB file using a provided transformer function.

    Args:
        path (str): Path to the input EPUB file.
        max_paragraphs (int): Maximum number of paragraphs to transform.
        transformer (Callable[[str], str]): Function to transform paragraph content.
    """
    book = epubfile.Epub(path)
    paragraphs_transformed = 0
    
    # Iterate through each text file in the EPUB
    for text_id in book.get_texts():
        if max_paragraphs > 0 and paragraphs_transformed >= max_paragraphs:
            break
        
        soup = book.read_file(text_id, soup=True)
        
        # Find all paragraphs
        all_paragraphs = {i: {"original": p, "transformed_outer_html": None} for i, p in enumerate(soup.find_all("p"))}
        
        # Concatenate to one big string
        combined_text = ""
        for paragraph_info in all_paragraphs.values():
            combined_text += str(paragraph_info["original"])
            
        if len(combined_text) == 0:
            continue
        
        # Transform all paragraphs
        transformed = transformer(combined_text)
        
        # Split the transformed text into paragraphs, keeping the </p> tag
        transformed_paragraphs = [p.strip() + '</p>' for p in transformed.split('</p>') if len(p.strip()) > 0]
        
        # Add transformed paragraphs to the dictionary
        for i, transformed_paragraph in enumerate(transformed_paragraphs):
            all_paragraphs[i]["transformed_outer_html"] = transformed_paragraph
            
        # Loop over the dictionary of paragraphs
        for i, paragraph_info in all_paragraphs.items():
            paragraph_info["original"].replace_with(BeautifulSoup(paragraph_info["transformed_outer_html"], 'html.parser'))

            paragraphs_transformed += 1
            if max_paragraphs > 0 and paragraphs_transformed >= max_paragraphs:
                break
        
        # Update file in book
        print("Updated file: " + text_id)
        book.write_file(text_id, soup)
        
    # Save the modified EPUB with a new filename
    output_path = f"{Path(path).stem}_out.epub"
    book.save(output_path)
    