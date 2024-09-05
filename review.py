import os
import json
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file']

def authenticate_google():
    """Authenticate the user with Google APIs using service account credentials."""
    creds = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), scopes=SCOPES)
    return build('docs', 'v1', credentials=creds), build('drive', 'v3', credentials=creds)

def upload_image_to_drive(image_path):
    """Upload an image to Google Drive and return its file ID."""
    _, drive_service = authenticate_google()
    file_metadata = {'name': os.path.basename(image_path)}
    media = MediaFileUpload(image_path, mimetype='image/png')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    drive_service.permissions().create(
        fileId=file.get('id'),
        body={'type': 'anyone', 'role': 'reader'},
    ).execute()

    return file.get('id')

def add_image_and_text_to_doc(doc_id, image_id, text):
    """Add a table with an image on the left and combined text on the right to the Google Doc."""
    doc_service, _ = authenticate_google()

    requests = [
        # Insert a table with 1 row and 2 columns at the start of the document
        {
            'insertTable': {
                'rows': 1,
                'columns': 2,
                'location': {
                    'index': 1,
                }
            }
        },

        # insert image.
        {
            'insertInlineImage': {
                'uri': f'https://drive.google.com/uc?id={image_id}',
                'location': {
                    'index': 5,
                },
                'objectSize': {
                    'height': {
                        'magnitude': 350,
                        'unit': 'PT'
                    },
                    'width': {
                        'magnitude': 350,
                        'unit': 'PT'
                    }
                }
            }
        },

        # Insert text into the first cell of the table
        {
            'insertText': {
                'location': {
                    'index': 8,
                },
                'text': text
            }
        },
    ]

    # Execute the batch update
    doc_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

def get_color_for_confidence(confidence):
    """Determine the text color based on the confidence level."""
    if confidence >= 0.95:
        return {'red': 0.0, 'green': 0.4, 'blue': 0.0}  # Dark Green
    elif confidence >= 0.85:
        return {'red': 1.0, 'green': 0.6, 'blue': 0.2}  # Orange
    else:
        return {'red': 0.7, 'green': 0.0, 'blue': 0.0}  # Dark Red

def digest_to_text(word_objects):
    """
    Converts the processed word objects into a single piece of text.
    Line breaks should be represented as newlines, and words should be separated by spaces.

    Args:
        word_objects: List of word objects with 'word', 'confidence', and 'detected_break'.

    Returns:
        A single string with proper spaces and line breaks.
    """
    text_lines = []
    current_line = []

    for word_obj in word_objects:
        word = word_obj['word']
        detected_break = word_obj['detected_break']

        # Add the word to the current line
        current_line.append(word)

        # If the detected break is a newline (3 or 5), flush the current line
        if detected_break in [3, 5]:
            text_lines.append(' '.join(current_line))
            current_line = []  # Start a new line

    # Add any remaining words that didn't trigger a newline
    if current_line:
        text_lines.append(' '.join(current_line))

    # Join all the lines with newlines and return the final text
    return '\n'.join(text_lines)

def main():
    parser = argparse.ArgumentParser(description="Populate a Google Doc with digests and images for manual review.")
    parser.add_argument('doc_id', help='ID of google doc to populate')
    parser.add_argument('image_file', help='Path to the image file')
    parser.add_argument('digest_file', help='Path to the digest JSON file')

    args = parser.parse_args()

    # Load environment variables
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # Check if the Google Application Credentials are set
    if not GOOGLE_APPLICATION_CREDENTIALS:
        raise EnvironmentError("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

    doc_id = args.doc_id
    image_path = args.image_file
    digest_path = args.digest_file

    # Verify that doc_id points to a valid document
    try:
        doc_service, _ = authenticate_google()
        doc_service.documents().get(documentId=doc_id).execute()
    except Exception as e:
        raise ValueError(f"The provided doc_id '{doc_id}' is not valid or accessible. Error: {e}")

    # Check if both digest and image files exist
    if not os.path.exists(digest_path) or not os.path.exists(image_path):
        print(f"Error: Both digest file '{digest_path}' and image file '{image_path}' must exist. Exiting.")
        exit(1)

    # Load digest content
    with open(digest_path, 'r', encoding='utf-8') as f:
        digest_data = json.load(f)

    # Upload image to Google Drive
    image_id = upload_image_to_drive(image_path)

    # Add the image and all text entries to the Google Doc as a single page
    digest_text = digest_to_text(digest_data)
    add_image_and_text_to_doc(doc_id, image_id, digest_text)

    print(f'Processed digest {digest_path} with image {image_path}')

if __name__ == '__main__':
    main()