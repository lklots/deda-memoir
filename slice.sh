# Define directories
PDF_DIR="pdfs"
IMG_DIR="slices"

# Initialize starting page number
start_page_num=1

# Loop through each PDF file in the directory
for pdf_file in "$PDF_DIR"/*.pdf; do

    # Extract the base name of the file (e.g., "Deda-1-20")
    base_name=$(basename "$pdf_file" .pdf)

    # Extract the last number from the base name to determine the end page number
    start_page_num=$(echo "$base_name" | grep -oE '[0-9]+' | head -1)

    # Construct the command to process the PDF file
    output_format="page_%03d.png"
    command="python pdf_to_images.py --start-page-num=$start_page_num --output-format=\"$output_format\" \"$pdf_file\" \"$IMG_DIR/\""

    # Execute the command
    echo "Processing: $pdf_file with start page $start_page_num"
    eval $command

done