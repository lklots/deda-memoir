#!/bin/bash

# Default input directories
REVISED_DIR="revised"
SLICES_DIR="slices"
DIGESTS_DIR="digests"
OUTPUT_DIR="reviews"

# Check if the revised directory exists
if [ ! -d "$REVISED_DIR" ]; then
    echo "Error: Input directory '$REVISED_DIR' does not exist."
    exit 1
fi

# Create the output directory if it doesn't exist
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    echo "Created output directory: $OUTPUT_DIR"
fi

# Get all JSON files and sort them numerically
files=($(ls "$REVISED_DIR"/page_*.json | sort -V))
total_files=${#files[@]}

# Process files in batches of 40
for ((i=0; i<$total_files; i+=40)); do
    start=$((i + 1))
    end=$((i + 40))
    if [ $end -gt $total_files ]; then
        end=$total_files
    fi

    # Create the output DOCX filename
    DOCX_FILE="$OUTPUT_DIR/review-$(printf %03d $start)-$(printf %03d $end).docx"

    echo "Processing batch $start to $end, output file: $DOCX_FILE"

    # Process each file in the current batch
    for ((j=i; j<end && j<total_files; j++)); do
        revised_file="${files[j]}"
        base_filename=$(basename "$revised_file")
        page_number=$(echo "$base_filename" | grep -oE '[0-9]+')

        slice_file="$SLICES_DIR/page_${page_number}.png"
        digest_file="$DIGESTS_DIR/${base_filename}"

        # Check if the slice and digest files exist
        if [ ! -f "$slice_file" ] || [ ! -f "$digest_file" ]; then
            echo "Error: Missing slice or digest file for $revised_file."
            continue
        fi

        echo "Reviewing $revised_file with $slice_file and $digest_file..."

        # Run the Python script and pass the JSON files as arguments
        python3 review.py "$DOCX_FILE" "$slice_file" "$digest_file" "$revised_file"

        review_status=$?

        # Check if the review process encountered an error
        if [ $review_status -ne 0 ]; then
            echo "Error: Failed to review $revised_file. Continuing with next file."
            continue
        fi

        echo "Reviewed $revised_file"
    done

    echo "Completed batch $start to $end"
done

echo "Review process complete."
