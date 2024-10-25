from langjoin import epub
from langjoin.replace import replace_noun_chunks

def main() -> int:
    replaced = replace_noun_chunks("The bear thinks about becoming a politician to make a greater impact on the world.", replace_func)
    print(replaced)
    return 0

def replace_func(input: str) -> str:
    if(input[0].isupper()):
        return "The man"
    else:
        return "the man"