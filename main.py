# main.py
import os
from src.utils.language_mapper import detect_language_and_translate
from src.scraper.content_scraper import scrape_topic_content
from src.extractor.multimodal_extractor import extract_multimodal_elements
from src.processing.preprocess import clean_text
from src.processing.structure_content import structure_content
from src.io.save_output import save_markdown_output, save_json_output

from tqdm import tqdm

PROMPT_FILE = "topic_query_prompts.txt"
OUTPUT_DIR = "output"

def load_prompts():
    topic_prompts = {}
    current_topic = "__DEFAULT__"
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "::" in line:
                topic, prompt = line.split("::", 1)
                topic_prompts[topic.strip()] = prompt.strip()
    return topic_prompts

def get_all_topics():
    topics_dir = "topics"
    all_topics = []
    for filename in os.listdir(topics_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(topics_dir, filename), "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        all_topics.append((filename.replace(".txt", ""), line))
    return all_topics

def main():
    topic_prompts = load_prompts()
    all_topics = get_all_topics()

    for domain, topic in tqdm(all_topics, desc="Processing Topics"):
        prompt_template = topic_prompts.get(domain, topic_prompts.get("__DEFAULT__"))
        full_prompt = prompt_template.replace("{topic}", topic)

        try:
            print(f"\n🔍 Scraping: {topic} [{domain}]")
            scraped_content = scrape_topic_content(full_prompt)

            if not scraped_content:
                print(f"❌ Skipping {topic}: No content found.")
                continue

            detected_text, lang = detect_language_and_translate(scraped_content)
            cleaned_text = clean_text(detected_text)

            multimodal_chunks = extract_multimodal_elements(cleaned_text, topic)
            structured_output = structure_content(cleaned_text, multimodal_chunks, topic)

            save_markdown_output(structured_output, domain, topic, OUTPUT_DIR)
            save_json_output(structured_output, domain, topic, OUTPUT_DIR)

            print(f"✅ Saved: {topic} [{domain}]")

        except Exception as e:
            print(f"⚠️ Error processing {topic}: {e}")

if __name__ == "__main__":
    main()
