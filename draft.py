import os
import re
from openai import OpenAI
from dotenv import load_dotenv
import argparse
import sys

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def format_text(text):
    prompt = f"""
        Take this draft of a book and make only white space formatting changes to it. Tell me what changes you made at a high-level.
        Desired Output: Provide the corrected version of the text. Do not prefix the output with any text.
        Then provide all the edits that were made prefixing that section with the string Edits:
        {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that formats text."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

def split_into_chunks(content, chunk_size=10000):
    chunks = []
    current_chunk = ""
    for page in re.split(r'(\[\[page_\d+\]\])', content):
        if page.startswith('[[page_'):
            if len(current_chunk) + len(page) > chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = page
            else:
                current_chunk += page
        else:
            if len(current_chunk) + len(page) > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = page
            else:
                current_chunk += page
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    chunks = split_into_chunks(content)
    formatted_content = ""
    all_changes = []

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...", file=sys.stderr)
        result = format_text(chunk)

        parts = result.split("\nEdits:", 1)
        if len(parts) == 2:
            formatted_text, change_description = parts
        else:
            formatted_text = parts[0]
            change_description = "No changes described."

        formatted_content += formatted_text
        all_changes.append(change_description.strip())

    # Write formatted content to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_content)

    print(f"Formatted text written to {output_file}", file=sys.stderr)
    print("\nFormatting changes:", file=sys.stderr)
    print("\n".join(all_changes), file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Format text using OpenAI's GPT-4 model.")
    parser.add_argument('input_file', help="Path to the input file containing the text to be formatted.")
    parser.add_argument('output_file', help="Path to the output file where the formatted text will be written.")
    args = parser.parse_args()

    process_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()