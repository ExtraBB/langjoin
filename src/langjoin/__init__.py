from langjoin.epub import transform_epub
from langjoin.transform_local import transform_text as transform_text_local
from langjoin.transform_llm import transform_text as transform_text_llm

def main() -> int:
    transform_epub("static/epub/monkey.epub", 5, epub_transformer)
    return 0

def test_transforms():
    text = "She got a mug from the cabinet. She set it beneath the machine’s dispenser. She opened the machine’s lid. Something began to buzz. She reached into the cabinet again. She retrieved an off-brand K-cup. The buzzing grew louder. She put the cup in the coffee maker. She closed the lid. The crunch felt violent. She selected ‘8oz’ on the little touch screen. The buzzing became a drone. She pressed the button beneath the touch screen. The machine began to whir. She could barely hear it over the droning. The floor creaked behind her. Something was watching her."
    transformed_local = transform_text_local(text, "pt", ["verb"], 0.7)
    transformed_llm = transform_text_llm(text, "pt", ["verb"], 0.7)
    print("LOCAL: " + transformed_local + "\n\n")
    print("LLM: " + transformed_llm + "\n\n")
    
def epub_transformer(text: str) -> str:
    return transform_text_llm(text, "pt", ["verb", "noun", "adjective"], 0.7)