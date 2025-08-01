# agents/multimodal_extractor.py

from bs4 import BeautifulSoup
from typing import Dict, List, Any
import base64
import re


class MultimodalExtractor:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")
        self.extracted: Dict[str, List[Any]] = {
            "text": [],
            "code": [],
            "images": [],
            "tables": [],
            "diagrams": []
        }

    def extract_text(self):
        """Extract visible text excluding code, tables, and nav elements."""
        for tag in self.soup.find_all(["p", "li", "span", "div", "section"]):
            if tag.find(["code", "pre", "table", "img", "svg"]):
                continue
            text = tag.get_text(strip=True)
            if text:
                self.extracted["text"].append(text)

    def extract_code(self):
        """Extract code blocks."""
        for tag in self.soup.find_all(["code", "pre"]):
            code = tag.get_text()
            if code and not code.isspace():
                self.extracted["code"].append(code)

    def extract_images(self):
        """Extract image sources (data URIs or links)."""
        for img in self.soup.find_all("img"):
            src = img.get("src")
            if src:
                self.extracted["images"].append(src)

    def extract_tables(self):
        """Extract tables as list of rows and cells."""
        for table in self.soup.find_all("table"):
            rows = []
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if cells:
                    rows.append(cells)
            if rows:
                self.extracted["tables"].append(rows)

    def extract_diagrams(self):
        """Extract embedded SVGs or diagram descriptions."""
        for svg in self.soup.find_all("svg"):
            self.extracted["diagrams"].append(str(svg))
        for canvas in self.soup.find_all("canvas"):
            self.extracted["diagrams"].append(str(canvas))

    def extract_all(self) -> Dict[str, List[Any]]:
        """Run all extractors."""
        self.extract_text()
        self.extract_code()
        self.extract_images()
        self.extract_tables()
        self.extract_diagrams()
        return self.extracted

    def summary(self) -> None:
        """Prints count of each modality."""
        print("[Multimodal Summary]")
        for key, value in self.extracted.items():
            print(f"  {key}: {len(value)} items")

