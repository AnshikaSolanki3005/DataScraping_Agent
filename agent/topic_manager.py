# agents/topic_manager.py

import os
import importlib.util
from pathlib import Path
from typing import Dict, Any, List

class TopicManager:
    def __init__(self, topic_dir: str = "topic_hierarchy"):
        self.topic_dir = Path(topic_dir)
        self.topic_trees: Dict[str, Any] = {}
        self.load_all_topics()

    def load_all_topics(self):
        """Load all Python files from topic_hierarchy/ and extract TOPIC_TREE dict."""
        for file in self.topic_dir.glob("*.py"):
            topic_name = file.stem
            topic_tree = self._load_topic_tree(file)
            if topic_tree:
                self.topic_trees[topic_name] = topic_tree

    def _load_topic_tree(self, filepath: Path) -> Dict[str, Any]:
        """Dynamically import a topic file and fetch its TOPIC_TREE."""
        spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            return getattr(module, "TOPIC_TREE", {})
        except Exception as e:
            print(f"[ERROR] Failed to load {filepath.name}: {e}")
            return {}

    def get_topic_names(self) -> List[str]:
        """List all loaded topic names."""
        return sorted(self.topic_trees.keys())

    def get_topic_tree(self, topic_name: str) -> Dict[str, Any]:
        """Return the topic tree for a specific subject."""
        return self.topic_trees.get(topic_name, {})

    def get_all_topics(self) -> Dict[str, Dict[str, Any]]:
        """Return all loaded topic trees."""
        return self.topic_trees

    def print_topic_tree(self, topic_name: str):
        """Pretty print the tree structure of a specific topic."""
        from rich import print as rprint
        from rich.tree import Tree

        topic_tree = self.get_topic_tree(topic_name)
        if not topic_tree:
            print(f"[WARN] No topic tree found for: {topic_name}")
            return

        def build_tree(node: Dict[str, Any], parent: Tree):
            for key, subnode in node.items():
                child = parent.add(f"[bold cyan]{key}[/]")
                if isinstance(subnode, dict):
                    build_tree(subnode, child)

        root = Tree(f"[green]{topic_name.upper()}[/]")
        build_tree(topic_tree, root)
        rprint(root)

