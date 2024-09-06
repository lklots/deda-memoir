#!/bin/bash

# Default input directories
REVISED_DIR="revised"
SLICES_DIR="slices"
DIGESTS_DIR="digests"
DOCX_FILE="review.docx"

# Check if the revised directory exists
if [ ! -d "$REVISED_DIR" ]; then
    echo "Error: Input directory '$REVISED_DIR' does not exist."
    exit 1
fi

# Loop through all JSON files in the revised directory
for revised_file in "$REVISED_DIR"/*.json; do
    # Check if file exists (in case there are no JSON files)
    [ -e "$revised_file" ] || continue

    # Get the base filename
    base_filename=$(basename "$revised_file")
    # Extract the page number from the filename
    page_number=$(echo "$base_filename" | grep -oE '[0-9]+')

    # Construct the corresponding slice file path with .png extension
    slice_file="$SLICES_DIR/page_${page_number}.png"
    digest_file="$DIGESTS_DIR/${base_filename}"

    # Check if the slice and digest files exist
    if [ ! -f "$slice_file" ]; then
        echo "Error: Slice file '$slice_file' does not exist for $revised_file."
        continue
    fi

    if [ ! -f "$digest_file" ]; then
        echo "Error: Digest file '$digest_file' does not exist for $revised_file."
        continue
    fi

    echo "Reviewing $revised_file with $slice_file and $digest_file..."

    # Run the Python script and pass the JSON files as arguments
    python3 review.py "$DOCX_FILE" "$slice_file" "$digest_file" "$revised_file"

    echo "Reviewed $revised_file"
done

echo "Review process complete."
