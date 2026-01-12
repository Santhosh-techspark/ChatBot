import re

def clean_llm_output(text: str) -> str:
    """
    Cleans LLM output to look like ChatGPT-style plain text.
    Removes markdown, tables, bullets, HTML tags.
    """

    if not text:
        return text

    # Remove markdown bold/italic
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # Remove markdown headings
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)

    # Remove markdown tables
    text = re.sub(r"\|.*\|", "", text)

    # Remove HTML line breaks
    text = re.sub(r"<br\s*/?>", "\n", text)

    # Remove extra bullet symbols
    text = re.sub(r"[-•]+", "", text)

    # Normalize whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
