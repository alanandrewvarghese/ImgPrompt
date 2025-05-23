import textwrap
import re

def format_prompt(prompt: str, width: int = 80) -> str:
    # Split prompt into sentences using regex to catch periods followed by space/newline
    sentences = re.split(r'(?<=\.)\s+', prompt.strip())

    # Wrap each sentence or chunk individually
    wrapped_sentences = [textwrap.fill(sentence, width=width) for sentence in sentences]

    # Join sentences with double newlines for paragraph breaks
    formatted_prompt = "\n\n".join(wrapped_sentences)
    return formatted_prompt
