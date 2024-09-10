# Set the PDF viewer
$pdf_previewer = 'open -a Skim';

# Set build and auxiliary directories
$out_dir = 'build';
$aux_dir = 'build';

# Check if a language flag is provided through the environment or command-line argument
my $languageflag = $ENV{'LANGUAGEFLAG'} || 'english';  # Default to 'english' if not set

# pdflatex command with the language flag and output file name
$pdflatex = "pdflatex -synctex=1 -output-directory=$out_dir \"\\newcommand{\\languageflag}{$languageflag}\\input{%S}\"";
