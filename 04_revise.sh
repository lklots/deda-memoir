#!/bin/bash

# Default input and output directories
INPUT_DIR=${1:-digests}
OUTPUT_DIR="revised"

# Check if the digests directory exists
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
# Loop through all JSON files in the digests directory
for file in "$INPUT_DIR"/*.json; do
    # Check if file exists (in case there are no JSON files)
    [ -e "$file" ] || continue

    # Get the base filename
    filename=$(basename "$file")
    # Define the output file path
    output_file="$OUTPUT_DIR/$filename"

    # Check if the revised file already exists
    if [ -f "$output_file" ]; then
        echo "$output_file already exists. Skipping..."
        continue
    fi
    # Process the file and capture the output in a temporary file
    temp_output=$(mktemp)
    if python revise.py "$file" > "$temp_output"; then
        # If successful, move the temporary file to the final output location
        mv "$temp_output" "$output_file"
        echo "Created $output_file"
    else
        echo "Error: Failed to process $file with revise.py."
        rm -f "$temp_output" # Clean up the temporary file
        continue
    fi

done

echo "Revision process complete."