#!/bin/bash

# Default input and output directories
INPUT_DIR=${1:-extracts}
OUTPUT_DIR="digests"

# Check if the input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist."
    exit 1
fi

# Create output directory if it does not exist
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create output directory '$OUTPUT_DIR'."
        exit 1
    fi
fi

# Check if there are any JSON files to process
if [ -z "$(ls -A $INPUT_DIR/page_*.json 2>/dev/null)" ]; then
    echo "Error: No JSON files found in the input directory '$INPUT_DIR'."
    exit 1
fi

# Loop through each JSON file in the input directory
for input_file in "$INPUT_DIR"/page_*.json; do
    # Check if the input file exists
    if [ ! -f "$input_file" ]; then
        echo "Warning: Input file '$input_file' does not exist or is not a file. Skipping."
        continue
    fi

    # Extract the file number from the input filename using sed
    file_number=$(basename "$input_file" .json | sed 's/page_//')

    # Set the output filename using the extracted file number
    output_file="$OUTPUT_DIR/page_digest_${file_number}.json"

    # Run the Python script and redirect output to the new file
    python3 digest.py "$input_file" > "$output_file"

    # Check if the Python script executed successfully
    if [ $? -ne 0 ]; then
        echo "Error: Failed to process '$input_file' with digest.py."
        rm -f "$output_file" # Clean up incomplete output file
        continue
    fi

    echo "Digested $input_file -> $output_file"
done
