#!/bin/bash
# Get current date and time
current_datetime=$(date "+%Y%m%d_%H%M")

# Output file
output_file="drafts/draft_ru_${current_datetime}.txt"

# Create drafts directory if it doesn't exist
mkdir -p drafts

# Clear the output file if it exists
> "$output_file"

# Loop through all JSON files in the revised/ directory, sorted numerically
for file in $(ls revised/page_*.json | sort -V); do
    # Extract the page number from the filename
    page_num=$(echo "$file" | sed -E 's/.*page_([0-9]+)\.json/\1/')

    # Check if page_num is empty and print an error if it is
    if [ -z "$page_num" ]; then
        echo "Error: Failed to extract page number from filename: $file" >&2
        continue
    fi

    # Add the page marker
    echo "[[page_$page_num]]" >> "$output_file"

    # Extract the "text" field from the JSON and append it to the output file
    jq -r '.text' "$file" >> "$output_file"

    # Add a newline after each page for readability
    echo "" >> "$output_file"
done

echo "Draft text has been written to $output_file"
