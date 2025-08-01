# main.py

import os
from tqdm import tqdm

from agent.language_mapper import detect_language_and_translate
from agent.content_scraper import ContentScraper
from agent.multimodal_extractor import MultimodalExtractor
from agent.topic_manager import TopicManager  # ✅ Added import

from pipeline.preprocess import Preprocessor
from pipeline.structure_content import ContentStructurer
from pipeline.save_output import OutputSaver

PROMPT_FILE = "topic_query_prompts.txt"
OUTPUT_DIR = "output"
TOPICS_DIR = "topics"

def load_prompts():
    topic_prompts = {}
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "::" in line:
                topic, prompt = line.split("::", 1)
                topic_prompts[topic.strip()] = prompt.strip()
    return topic_prompts

def get_all_topics():
    all_topics = []
    for filename in os.listdir(TOPICS_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(TOPICS_DIR, filename), "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        all_topics.append((filename.replace(".txt", ""), line.strip()))
    return all_topics

def main():
    topic_prompts = load_prompts()
    all_topics = get_all_topics()

    # ✅ Initialize components
    topic_manager = TopicManager()  # ✅ Added initialization
    scraper = ContentScraper(topic_manager=topic_manager)  # ✅ Pass it here
    preprocessor = Preprocessor()
    structurer = ContentStructurer()
    saver = OutputSaver(output_dir=OUTPUT_DIR)

    for domain, topic in tqdm(all_topics, desc="Processing Topics"):
        prompt_template = topic_prompts.get(domain, topic_prompts.get("__DEFAULT__"))
        full_prompt = prompt_template.replace("{topic}", topic)

        try:
            print(f"\n🔍 Scraping: {topic} [{domain}]")

            # Step 1: Scrape content
            scraped_content = scraper.scrape_content(full_prompt)
            if not scraped_content:
                print(f"❌ Skipping {topic}: No content found.")
                continue

            # Step 2: Translate if needed
            detected_text, lang = detect_language_and_translate(scraped_content)

            # Step 3: Clean text
            cleaned_text = preprocessor.preprocess_text(detected_text)

            # Step 4: Extract multimodal elements
            extractor = MultimodalExtractor(html=cleaned_text)
            multimodal_chunks = extractor.extract_all()

            # Step 5: Structure the content
            structured_output = structurer.structure_content(cleaned_text, multimodal_chunks, topic)

            # Step 6: Save outputs
            filename = f"{domain}_{topic.replace(' ', '_')}"
            saver.save_as_markdown(filename, structured_output)
            saver.save_as_json(filename, structured_output)

            print(f"✅ Saved: {topic} [{domain}]")

        except Exception as e:
            print(f"⚠️ Error processing {topic}: {e}")

if __name__ == "__main__":
    main()
