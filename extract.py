import os
import io
import argparse
from google.cloud import vision
from google.auth.exceptions import DefaultCredentialsError

# Load environment variables
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Check if the Google Application Credentials are set
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise EnvironmentError("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

# Initialize the Google Cloud Vision client
try:
    client = vision.ImageAnnotatorClient()
except DefaultCredentialsError as e:
    raise DefaultCredentialsError(f"Failed to authenticate with Google Cloud: {e}")

def extract_text_from_image(image_path):
    """
    Extracts text from an image using Google Cloud Vision API.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Extracted text from the image.
    """
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The specified image file does not exist: {image_path}")

    try:
        # Load image into memory
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        # Perform text detection on the image
        response = client.document_text_detection(image=image)

        # Check for errors in the response
        if response.error.message:
            raise Exception(f"Error during text detection: {response.error.message}")

        # Return extracted text
        return response.full_text_annotation.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Extract text from an image using Google Cloud Vision API.')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    args = parser.parse_args()

    # Extract text from the specified image
    extracted_text = extract_text_from_image(args.image_path)

    if extracted_text:
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("No text extracted or an error occurred.")

if __name__ == "__main__":
    main()
