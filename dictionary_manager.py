import json
import os
import re

def is_kana(text):
    """Check if the text contains only Kana characters (Hiragana and Katakana)."""
    kana_re = re.compile(r'^[\u3040-\u309F\u30A0-\u30FF]+$')
    return kana_re.match(text) is not None

def load_dictionaries(dictionary_files):
    dictionaries = []
    for file_path in dictionary_files:
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:  # Use utf-8-sig to handle BOM
                dictionary = json.load(file)
                dictionary_name = os.path.basename(file_path)  # Use the file name as the dictionary name
                dictionaries.append((dictionary_name, dictionary))
        except Exception as e:
            print(f"Error reading dictionary file {file_path}: {e}")
    return dictionaries

def fetch_readings_and_definitions(selected_text, dictionaries):
    readings = []
    definitions = []
    examples = []

    for dictionary_name, dictionary in dictionaries:
        for word in dictionary.get('words', []):
            for kanji_entry in word.get('kanji', []):
                if kanji_entry['text'] == selected_text:
                    for kana_entry in word.get('kana', []):
                        readings.append(kana_entry['text'])
                    for sense in word.get('sense', []):
                        for gloss in sense.get('gloss', []):
                            definitions.append(f"• {gloss['text']}")
                        for example in sense.get('examples', []):
                            for sentence in example.get('sentences', []):
                                examples.append(f"• {sentence['text']}")
            # Check kana entries for hiragana words
            for kana_entry in word.get('kana', []):
                if kana_entry['text'] == selected_text:
                    if not is_kana(selected_text):  # Only add readings if the text is not Kana-only
                        readings.append(kana_entry['text'])
                    for sense in word.get('sense', []):
                        for gloss in sense.get('gloss', []):
                            definitions.append(f"• {gloss['text']}")
                        for example in sense.get('examples', []):
                            for sentence in example.get('sentences', []):
                                examples.append(f"• {sentence['text']}")
    return readings, definitions, examples