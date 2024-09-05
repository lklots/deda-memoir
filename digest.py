import json
import argparse
import sys

import enchant

def digest(json_data):
    """
    Process the fullTextAnnotation object from the given JSON data.
    Extract words, their confidence levels, and detected breaks.
    """
    word_objects = []

    try:
        full_text_annotation = json_data.get("fullTextAnnotation", {})
        if not full_text_annotation:
            raise ValueError("Missing 'fullTextAnnotation' in JSON data.")

        for page in full_text_annotation.get("pages", []):
            for block in page.get("blocks", []):
                for paragraph in block.get("paragraphs", []):
                    words = paragraph.get("words", [])

                    for word in words:
                        # Concatenate text from all symbols within each word
                        word_text = ''.join([symbol.get("text", "") for symbol in word.get("symbols", [])])

                        # Extract confidence of the paragraph
                        confidence = word.get("confidence", 0.0)

                        # Initialize detected break as empty
                        detected_break = ''

                        # Check symbols for detectedBreak metadata
                        for symbol in word.get("symbols", []):
                            symbol_property = symbol.get("property", {})
                            if "detectedBreak" in symbol_property:
                                detected_break = symbol_property["detectedBreak"].get("type", "")

                        # Add the word with its metadata to the list
                        word_objects.append({
                            "word": word_text,
                            "confidence": confidence,
                            "detected_break": detected_break
                        })

        return word_objects

    except KeyError as e:
        raise ValueError(f"Expected key missing in JSON data: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing the JSON data: {e}")


def combine_words_on_newline_break(word_objects):
    """
    Combine words with a newline detected break if the combined word exists in the dictionary.
    The detected break and confidence of the first word will be preserved.

    Args:
        word_objects: List of word objects with 'word', 'confidence', and 'detected_break'.
        dictionary: Set of valid words in Russian to check against.

    Returns:
        Modified list of word objects with combined words where applicable.
    """
    combined_result = []
    i = 0

    while i < len(word_objects):
        word_obj = word_objects[i]
        current_word = word_obj["word"]
        detected_break = word_obj["detected_break"]
        confidence = word_obj["confidence"]

        # Check if the detected break is a newline (3 or 5)
        if detected_break in [3, 5] and i + 1 < len(word_objects):
            # Get the next word
            next_word_obj = word_objects[i + 1]
            next_word = next_word_obj["word"]

            # Remove trailing hyphen
            if current_word.endswith('-'):
                current_word = current_word[:-1]

            # Try to combine the current word and the next word
            combined_word = current_word + next_word

            # Check if the combined word exists in the dictionary
            if is_valid_russian_word(combined_word):
                # If valid, replace the two words with the combined word
                combined_result.append({
                    "word": combined_word,
                    "confidence": confidence,  # Keep the confidence of the first word
                    "detected_break": detected_break  # Preserve the detected break of the first word
                })
                # Skip the next word since it's already combined
                i += 2
                continue

        # If no combination happens, add the current word as it is
        combined_result.append(word_obj)
        i += 1

    return combined_result


def is_valid_russian_word(word):
    return russian_dict.check(word)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process a JSON file to extract full text annotation into sentences with confidence.")
    parser.add_argument("input_file", help="Path to the input JSON file.")
    args = parser.parse_args()

    # Initialize a Russian dictionary
    global russian_dict
    russian_dict = enchant.Dict("ru_RU")
    try:
        # Load the JSON data from the input file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Process the JSON data to extract sentences and confidence
        processed_data = digest(json_data)
        processed_data = combine_words_on_newline_break(processed_data)

        # Output the result as JSON to stdout
        print(json.dumps(processed_data, ensure_ascii=False, indent=2))

    except FileNotFoundError:
        sys.stderr.write(f"Error: The file '{args.input_file}' was not found.\n")
        sys.exit(1)
    except json.JSONDecodeError:
        sys.stderr.write("Error: Failed to decode JSON. Please check the input file format.\n")
        sys.exit(1)
    except ValueError as ve:
        sys.stderr.write(f"Error: {ve}\n")
        sys.exit(1)
    except RuntimeError as re:
        sys.stderr.write(f"Error: {re}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

