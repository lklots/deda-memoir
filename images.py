import fitz  # PyMuPDF
import os
import argparse
import sys

def pdf_to_images(pdf_path, output_folder, start_page_num, output_format):
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error: Unable to open PDF file '{pdf_path}'. {e}")
        sys.exit(1)

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            print(f"Error: Unable to create output folder '{output_folder}'. {e}")
            sys.exit(1)

    # Iterate over each page
    try:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # load the page
            pix = page.get_pixmap()  # render the page to an image
            # Use the output format string to generate the filename
            image_filename = output_format % (start_page_num + page_num)
            image_path = os.path.join(output_folder, image_filename)
            pix.save(image_path)  # save the image as PNG
            print(f"Saved: {image_path}")
    except Exception as e:
        print(f"Error: An error occurred while processing the PDF. {e}")
        sys.exit(1)

    # Close the PDF file
    doc.close()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert PDF pages to images.")
    parser.add_argument("pdf_path", type=str, help="Path to the input PDF file")
    parser.add_argument("output_folder", type=str, help="Folder to save output images")
    parser.add_argument("--start-page-num", type=int, default=1, help="Starting page number for output file names (default is 1)")
    parser.add_argument("--output-format", type=str, default="page_%03d.png",
                        help="Format for output filenames, using a printf-style placeholder for the page number (default is 'page_%03d.png')")

    # Parse arguments
    args = parser.parse_args()

    # Validate PDF file path
    if not os.path.isfile(args.pdf_path):
        print(f"Error: The file '{args.pdf_path}' does not exist or is not a valid file.")
        sys.exit(1)

    # Convert PDF to images
    pdf_to_images(args.pdf_path, args.output_folder, args.start_page_num, args.output_format)

if __name__ == "__main__":
    main()
