import json
import argparse
import sys

def process_full_text_annotation(json_data):
    """
    Process the fullTextAnnotation object from the given JSON data.
    Extract sentences and their confidence levels.
    """
    sentence_objects = []
    try:
        full_text_annotation = json_data.get("fullTextAnnotation", {})
        if not full_text_annotation:
            raise ValueError("Missing 'fullTextAnnotation' in JSON data.")

        for page in full_text_annotation.get("pages", []):
            for block in page.get("blocks", []):
                for paragraph in block.get("paragraphs", []):
                    # Concatenate text from all symbols within each word, then join words with spaces
                    sentence_text = ' '.join(
                        [''.join([symbol.get("text", "") for symbol in word.get("symbols", [])])
                         for word in paragraph.get("words", [])]
                    )
                    # Get confidence from the paragraph
                    confidence = paragraph.get("confidence", 0.0)

                    # Add sentence and confidence to the result list
                    sentence_objects.append({
                        "text": sentence_text,
                        "confidence": confidence
                    })

        return sentence_objects

    except KeyError as e:
        raise ValueError(f"Expected key missing in JSON data: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing the JSON data: {e}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process a JSON file to extract full text annotation into sentences with confidence.")
    parser.add_argument("input_file", help="Path to the input JSON file.")
    args = parser.parse_args()

    try:
        # Load the JSON data from the input file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Process the JSON data to extract sentences and confidence
        processed_data = process_full_text_annotation(json_data)

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

