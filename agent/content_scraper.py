# agents/content_scraper.py

from typing import Dict, Any
from agents.topic_manager import TopicManager
import json
from pathlib import Path
import time
import random


class ContentScraper:
    def __init__(self, topic_manager: TopicManager):
        self.topic_manager = topic_manager
        self.scraped_data: Dict[str, Dict[str, str]] = {}

    def scrape_all_topics(self):
        """Scrape all topics loaded by TopicManager."""
        topics = self.topic_manager.get_topic_names()
        for topic in topics:
            print(f"\n[INFO] Scraping topic: {topic}")
            tree = self.topic_manager.get_topic_tree(topic)
            self.scraped_data[topic] = {}
            self._recursive_scrape(topic, tree)

    def _recursive_scrape(self, topic_name: str, tree: Dict[str, Any], parent_path: str = ""):
        """Recursively traverse the topic tree and scrape content."""
        for subtopic, subnodes in tree.items():
            full_path = f"{parent_path}/{subtopic}" if parent_path else subtopic
            print(f"    ➤ Scraping: {full_path}")
            content = self._scrape_content(full_path)
            self.scraped_data[topic_name][full_path] = content
            if isinstance(subnodes, dict):
                self._recursive_scrape(topic_name, subnodes, full_path)

    def _scrape_content(self, topic_path: str) -> str:
        """
        Replace this stub with real scraping/generation logic.
        For now, it simulates delay and returns a placeholder string.
        """
        time.sleep(random.uniform(0.1, 0.3))  # Simulate scraping delay
        return f"📘 Content for: {topic_path}"

    def save_to_json(self, output_dir="scraped_data"):
        """Save the scraped data as structured JSON files, one per topic."""
        Path(output_dir).mkdir(exist_ok=True)
        for topic, data in self.scraped_data.items():
            out_path = Path(output_dir) / f"{topic}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[✓] Saved: {out_path}")

    def save_to_markdown(self, output_dir="scraped_data_markdown"):
        """Save each topic’s content as a Markdown document."""
        Path(output_dir).mkdir(exist_ok=True)
        for topic, data in self.scraped_data.items():
            out_path = Path(output_dir) / f"{topic}.md"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(f"# {topic.replace('_', ' ').title()}\n\n")
                for path, content in data.items():
                    indent_level = path.count("/")
                    heading = "#" * (indent_level + 2)
                    f.write(f"{heading} {path.split('/')[-1]}\n\n")
                    f.write(f"{content}\n\n")
            print(f"[✓] Saved: {out_path}")
