# pipeline/save_output.py

import os
import json
from typing import Dict


class OutputSaver:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_as_json(self, topic_name: str, data: Dict):
        """
        Save structured data as a JSON file under the topic's name.
        """
        filename = os.path.join(self.output_dir, f"{topic_name}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[✔] Saved JSON: {filename}")

    def save_as_markdown(self, topic_name: str, content_dict: Dict):
        """
        Save structured content in Markdown format.
        """
        filename = os.path.join(self.output_dir, f"{topic_name}.md")
        with open(filename, "w", encoding="utf-8") as f:
            for heading, content in content_dict.items():
                level = heading.count('.') + 1 if '.' in heading else 2
                markdown_heading = "#" * level + " " + heading
                f.write(f"{markdown_heading}\n\n{content.strip()}\n\n")
        print(f"[✔] Saved Markdown: {filename}")

    def save_as_text(self, topic_name: str, content_dict: Dict):
        """
        Save as plain .txt file (optional, for simplicity).
        """
        filename = os.path.join(self.output_dir, f"{topic_name}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            for heading, content in content_dict.items():
                f.write(f"{heading.upper()}\n{'=' * len(heading)}\n{content.strip()}\n\n")
        print(f"[✔] Saved TXT: {filename}")

    def save_all(self, topic_name: str, structured_data: Dict, save_md=True, save_txt=False):
        """
        Save hierarchy and topic content as multiple formats.
        """
        self.save_as_json(topic_name, structured_data)

        if save_md:
            self.save_as_markdown(topic_name, structured_data.get("topic_content", {}))

        if save_txt:
            self.save_as_text(topic_name, structured_data.get("topic_content", {}))
