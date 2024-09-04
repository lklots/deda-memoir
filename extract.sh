#!/bin/bash

# Directories
INPUT_DIR="slices"
OUTPUT_DIR="extracts"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Iterate over all image files in the input directory
for image_file in "$INPUT_DIR"/*.png; do
    # Get the base filename without the directory or extension
    base_filename=$(basename "$image_file" .png)

    # Define the corresponding JSON file path in the output directory
    json_file="$OUTPUT_DIR/$base_filename.json"

    # Check if the JSON file already exists
    if [ -f "$json_file" ]; then
        # If it exists, output a message with the last modified date
        last_modified=$(stat -c %y "$json_file")
        echo "$json_file already exists. Last modified: $last_modified"
    else
        # If it doesn't exist, run the extraction script and save the output
        echo "Processing $image_file..."
        if python extract.py "$image_file" > "$json_file"; then
            echo "Saved output to $json_file"
        else
            # If extract.py returns a non-zero exit code, handle the error
            echo "Error: Failed to process $image_file. Removing incomplete $json_file."
            # Remove the incomplete JSON file to avoid confusion
            rm -f "$json_file"
        fi
    fi
done
