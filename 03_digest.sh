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

# Export the necessary variables for parallel execution
export INPUT_DIR OUTPUT_DIR

# Function to process a single JSON file
process_file() {
    input_file=$1
    file_number=$(basename "$input_file" .json | sed 's/page_//')
    output_file="$OUTPUT_DIR/page_digest_${file_number}.json"
    python3 digest.py "$input_file" > "$output_file"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to process '$input_file' with digest.py."
        rm -f "$output_file" # Clean up incomplete output file
    else
        echo "Digested $input_file -> $output_file"
    fi
}

# Export the function for parallel execution
export -f process_file

# Find all JSON files and process them in parallel
find "$INPUT_DIR" -name 'page_*.json' -print0 | xargs -0 -n 1 -P 4 bash -c 'process_file "$0"'
