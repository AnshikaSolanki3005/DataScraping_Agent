# pipeline/preprocess.py

import re
from bs4 import BeautifulSoup


class Preprocessor:
    def __init__(self, remove_html=True, normalize_whitespace=True):
        self.remove_html = remove_html
        self.normalize_whitespace = normalize_whitespace

    def clean_html(self, content: str) -> str:
        """
        Removes HTML tags from content using BeautifulSoup.
        """
        return BeautifulSoup(content, "html.parser").get_text()

    def normalize_spaces(self, text: str) -> str:
        """
        Normalizes spaces, tabs, and newlines to a clean structure.
        """
        text = re.sub(r'\r', '', text)
        text = re.sub(r'\n{2,}', '\n\n', text)  # condense multiple newlines
        text = re.sub(r'[ \t]+', ' ', text)  # replace multiple spaces/tabs with one
        return text.strip()

    def remove_special_chars(self, text: str) -> str:
        """
        Optionally remove unwanted characters (e.g., non-UTF8 garbage).
        """
        return re.sub(r'[^\x00-\x7F]+', '', text)

    def preprocess_text(self, raw_content: str) -> str:
        """
        Cleans and formats raw content for structuring and analysis.
        """
        if self.remove_html:
            raw_content = self.clean_html(raw_content)
        if self.normalize_whitespace:
            raw_content = self.normalize_spaces(raw_content)

        cleaned = self.remove_special_chars(raw_content)
        return cleaned

    def extract_code_blocks(self, text: str) -> list:
        """
        Extracts code blocks surrounded by triple backticks (```) or indents.
        """
        code_blocks = re.findall(r'```(?:\w+)?(.*?)```', text, re.DOTALL)
        return [cb.strip() for cb in code_blocks if cb.strip()]

    def split_text_sections(self, content: str) -> list:
        """
        Splits the text into meaningful paragraphs or sections.
        """
        return [para.strip() for para in content.split('\n\n') if para.strip()]
