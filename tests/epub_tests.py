import unittest
from pathlib import Path
from langjoin import transform_epub
from langjoin.transformers.transform_mock import transform_text as transform_text_mock
import epubfile

class TestEpubTransformation(unittest.TestCase):
    def transform_epub_with_mock_should_not_change_contents(self):
        # Path to the test EPUB file
        input_path = "static/epub/monkey.epub"
        
        # Define the mock transformer
        mock_transformer = lambda text: transform_text_mock(text, "pt", ["verb", "noun", "adjective"], 0.7)
        
        # Transform the EPUB using the mock transformer
        transform_epub(input_path, 5, mock_transformer)
        
        # Path to the transformed EPUB file
        output_path = f"{Path(input_path).stem}_out.epub"
        
        # Read and compare HTML content of both EPUBs
        original_book = epubfile.Epub(input_path)
        transformed_book = epubfile.Epub(output_path)
        
        for text_id in original_book.get_texts():
            original_soup = original_book.read_file(text_id, soup=True)
            transformed_soup = transformed_book.read_file(text_id, soup=True)
            
            # Compare the HTML contents
            self.assertEqual(str(original_soup), str(transformed_soup))
        
        
        # Clean up the transformed file
        Path(output_path).unlink()

if __name__ == "__main__":
    unittest.main()
