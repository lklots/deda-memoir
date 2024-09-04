# Deda Memoir

This project automates the process of transcribing Deda's handwritten memoirs from PDF format to text using Google Cloud Vision API.

## Components

1. **slice**: Converts PDF memoirs into individual page images.
2. **extract**: Uses Google Cloud Vision API to extract handwritten text from images.

## Prerequisites

- Python 3.x
- Google Cloud account with Vision API enabled
- `GOOGLE_APPLICATION_CREDENTIALS` environment variable set to the path of your Google Cloud service account key JSON file. To obtain this key:
  1. Create a service account in the Google Cloud Console
  2. Generate a JSON key for the service account
  3. Download the JSON key file
  4. Set the environment variable to the path of the downloaded file

  For detailed instructions, refer to the Google Cloud documentation:
  https://cloud.google.com/docs/authentication/getting-started

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
  ```
  source venv/bin/activate
  ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Workflow

1. Convert the PDF memoir in pdfs/ to images using `process_pdfs.sh`
2. For each resulting image, use `extract.py` to transcribe the handwritten text


