from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

class LanguageMapper:
    def __init__(self):
        pass

    def detect_language(self, code: str) -> str:
        """
        Detects the programming language of a given code snippet using Pygments.
        Returns a string like 'Python', 'C++', 'HTML', etc.
        """
        try:
            lexer = guess_lexer(code)
            return lexer.name
        except ClassNotFound:
            return "Unknown"

    def map_language_to_filetype(self, lang_name: str) -> str:
        """
        Maps a lexer language name to a standard file extension/type.
        Useful for saving or categorizing snippets.
        """
        mapping = {
            "Python": "py",
            "C++": "cpp",
            "C": "c",
            "Java": "java",
            "JavaScript": "js",
            "HTML": "html",
            "CSS": "css",
            "JSON": "json",
            "SQL": "sql",
            "Bash": "sh",
            "Markdown": "md",
            "XML": "xml",
            "YAML": "yml",
            "Unknown": "txt"
        }
        return mapping.get(lang_name, "txt")

    def get_language_info(self, code: str) -> dict:
        """
        Returns both the language name and file type.
        """
        lang_name = self.detect_language(code)
        file_type = self.map_language_to_filetype(lang_name)
        return {"language": lang_name, "file_type": file_type}


def detect_language_and_translate(code: str) -> dict:
    """
    Standalone wrapper function to detect language and file type.
    """
    mapper = LanguageMapper()
    return mapper.get_language_info(code)
