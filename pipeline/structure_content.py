# pipeline/structure_content.py

import re
from typing import List, Dict


class ContentStructurer:
    def __init__(self):
        self.topic_structure = {}

    def detect_topic_hierarchy(self, lines: List[str]) -> List[Dict[str, str]]:
        """
        Detect headings and structure them based on markdown-like syntax or heuristics.
        Returns a list of dicts with level and title.
        """
        hierarchy = []
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect headings using markdown symbols or numbering
            if line.startswith("#"):
                level = line.count("#")
                title = line.replace("#", "").strip()
                hierarchy.append({"level": level, "title": title})
            elif re.match(r"^\d+(\.\d+)*\s", line):  # numbered headings
                depth = line.count(".") + 1
                title = re.sub(r"^\d+(\.\d+)*\s+", "", line)
                hierarchy.append({"level": depth, "title": title})
            elif line.isupper():
                # ALL CAPS can be section headers
                hierarchy.append({"level": 1, "title": line.title()})

        return hierarchy

    def build_hierarchy_tree(self, headings: List[Dict[str, str]]) -> Dict:
        """
        Builds a nested dictionary tree of the headings and their levels.
        """
        tree = {}
        stack = [(0, tree)]  # (level, dict)

        for item in headings:
            level = item["level"]
            title = item["title"]

            while stack and stack[-1][0] >= level:
                stack.pop()

            parent = stack[-1][1]
            parent[title] = {}
            stack.append((level, parent[title]))

        return tree

    def attach_content_to_hierarchy(self, text: str) -> Dict:
        """
        Organizes content into a hierarchy based on markdown headings and surrounding content.
        """
        sections = re.split(r"(?:^|\n)(#+ .+)", text)
        structured = {}
        current_key = "Introduction"

        for i in range(1, len(sections), 2):
            heading = sections[i].strip().replace("#", "").strip()
            content = sections[i + 1].strip()
            structured[heading] = content

        return structured

    def structure_content(self, cleaned_text: str) -> Dict:
        """
        Full pipeline to extract and structure headings and their associated content.
        """
        lines = cleaned_text.splitlines()
        headings = self.detect_topic_hierarchy(lines)
        tree = self.build_hierarchy_tree(headings)
        content_blocks = self.attach_content_to_hierarchy(cleaned_text)
        return {
            "hierarchy_tree": tree,
            "topic_content": content_blocks
        }
