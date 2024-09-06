# Deda Memoir

This project automates the process of transcribing Deda's handwritten memoirs from PDF format to text using Google Cloud Vision API and OpenAI.

## Prerequisites

- Python 3.x
- Google cloud environment. See next section
- To support Russian dictionary lookups in the `03_digest.sh` step, you need to install the `enchant` library with Russian dictionary support. Follow these steps:

1. Install `enchant` using Homebrew:
   ```
   brew install enchant
   ```

2. Verify the installation:
   ```
   enchant-lsmod-2
   ```

3. Ensure the Russian dictionary is available. If not, you may need to install the `hunspell-ru` package:
   ```
   brew install hunspell-ru
   ```

4. Verify that the Russian dictionary is listed:
   ```
   enchant-lsmod-2 | grep ru_RU
   ```

## Configuring the Google Cloud Environment (steps not verified)

To configure the Google Cloud environment for this project, follow these steps:

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing project.

2. **Enable Required APIs**:
   - Enable the following APIs for your project:
     - Google Docs API
     - Google Drive API
     - Cloud Vision API
   - You can enable these APIs by navigating to the "APIs & Services" > "Library" section in the Google Cloud Console and searching for each API.

3. **Create a Service Account**:
   - In the Google Cloud Console, go to "IAM & Admin" > "Service Accounts".
   - Click "Create Service Account".
   - Provide a name and description for the service account, then click "Create".

4. **Grant Permissions to the Service Account**:
   - Assign the following roles to the service account:
     - `roles/docs.editor` (Google Docs API)
     - `roles/drive.file` (Google Drive API)
     - `roles/vision.user` (Cloud Vision API)
   - These roles can be assigned during the service account creation process or later by editing the service account permissions.

5. **Generate and Download the Service Account Key**:
   - After creating the service account, go to the "Keys" section.
   - Click "Add Key" > "Create New Key".
   - Select "JSON" as the key type and click "Create".
   - Download the JSON key file to your local machine.

6. **Set the `GOOGLE_APPLICATION_CREDENTIALS` Environment Variable**:
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the downloaded JSON key file. This can be done by running the following command in your terminal:
     ```sh
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
     ```

7. **Verify Enabled Services**:
   - Ensure that the following services are enabled in your Google Cloud project:
     ```sh
     gcloud services list --enabled
     ```
     The output should include a subset of the following services:
     ```
     NAME                                TITLE
     docs.googleapis.com                 Google Docs API
     drive.googleapis.com                Google Drive API
     vision.googleapis.com               Cloud Vision API
     ```

By following these steps, you will have the necessary Google Cloud environment configured for this project.

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

The project consists of several shell scripts that should be run in order. Here's a description of each script:

1. **01_slice.sh**:
   - Description: Converts the PDF memoir into individual page images.
   - Outputs: Image files in the `slices/` directory.
   - Usage: `./01_slice.sh`

2. **02_extract.sh**:
   - Description: Uses Google Cloud Vision API to extract handwritten text from the images.
   - Outputs: Individual text files in the `extracts/` directory.
   - Usage: `./02_extract.sh`

3. **03_digest.sh**:
   - Description: Processes the extracted text files to create a more compact and accurate representation, including Russian dictionary lookups.
   - Outputs: Processed text files in the `digests/` directory.
   - Usage: `./03_digest.sh`

4. **04_revise.sh**:
   - Description: Uses OpenAI to refine the text, producing a more polished output.
   - Outputs: Refined text files in the `revised/` directory.
   - Usage: `./04_revise.sh`

5. **05_review.sh**:
   - Description: populates a doc with all the information necessary to make a manual review.
   - Outputs: Final transcribed and reviewed memoir file in the output directory.
   - Usage: `./05_review.sh`







