import argparse
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def load_json(file_path):
    """Loads the JSON data from the provided file path."""
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def assemble_text(ocr_data):
    """Assembles OCR data from JSON into a single text string while respecting detected_break values."""
    text = ""
    for item in ocr_data:
        word = item['word']
        detected_break = item.get('detected_break', '')

        # Append the word to the text
        text += word

        # Handle the detected break types
        if detected_break == 1:  # Space break
            text += " "
        elif detected_break == 3:  # Line break
            text += "\n"
        elif detected_break == 5:  # Line break (not paragraph break)
            text += "\n\n"

    return text.strip()  # Remove any leading or trailing whitespace

def refine_text_with_openai(text):
    """Sends the assembled text to OpenAI API for refinement."""
    prompt = f"""
      i am transcribing a russian book.
      i need you to take this ocred text and tell which errors exist.
      then re-write the text as necessary.
      finally, provide basic formatting for things like quotes and others to make it easier to convert to a book.
      try to keep the text as close to the original as possible. keep page references.

      {text}

      Desired Output: Provide the corrected version of the text. Do not prefix the output with any text.
      Then provide all the edits that were made prefixing that section with the string Edits:
    """

    # Make a call to the OpenAI API for text refinement
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert editor with a focus on maintaining accuracy in transcriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    # Extract the content and edits from the assistant's message
    content = response.choices[0].message.content

    # Split the content into corrected text and edits
    corrected_text, edits_section = content.split("Edits:", 1)

    format_prompt = f"""
    Take this text and clean up all spacing issues. Specifically:
    - Remove all extra spaces between words or after punctuation marks.
    - Remove all unnecessary newlines and tabs.
    - Ensure a single space separates sentences and paragraphs are distinct.

    Desired Output: Provide the formatted version of the text. Do not prefix the output with any text.
    Then provide all the edits that were made prefixing that section with the string Edits:

    {corrected_text}
    """

    format_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful editor that formats books."},
            {"role": "user", "content": format_prompt}
        ],
        temperature=0.7,
    )

    # Extract formatted text and formatting edits
    format_content = format_response.choices[0].message.content
    formatted_text, format_edits = format_content.split("Edits:", 1)
    formatted_text = formatted_text.strip()
    format_edits = format_edits.strip()

    # Combine both sets of edits
    combined_edits = f"{edits_section.strip()}\n\nFormatting edits:\n{format_edits}"

    return formatted_text, combined_edits

def main(json_file):
    # Load the OCR data from JSON file
    ocr_data = load_json(json_file)

    # Assemble OCR words into raw text while respecting breaks
    raw_text = assemble_text(ocr_data)

    # Refine the raw text using OpenAI API
    corrected_text, edits = refine_text_with_openai(raw_text)

    # Create the output as a JSON object
    output = {
        "text": corrected_text,
        "edits": edits
    }

    # Print the JSON object to stdout
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Process a JSON OCR data to generate a page of text.')
    parser.add_argument('json_file', type=str, help='The JSON file containing the OCR-extracted text.')

    # Parse the arguments
    args = parser.parse_args()

    # Run the main process
    main(args.json_file)
