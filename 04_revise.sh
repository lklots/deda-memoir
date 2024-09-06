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

    # Replace _digest with _revised in the filename
    revised_filename="${filename/_digest/_revised}"

    echo "Processing $filename..."

    # Run the Python script and redirect output to the new file
    python revise.py "$file" > "revised/$revised_filename"

    echo "Created revised/$revised_filename"
done

echo "Revision process complete."