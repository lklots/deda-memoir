# Set the PDF viewer
$pdf_previewer = 'open -a Skim';

# Set build and auxiliary directories
$out_dir = 'build';
$aux_dir = 'build';

# Check if a language flag is provided through the environment or command-line argument
my $languageflag = $ENV{'LANGUAGEFLAG'} || 'english';  # Default to 'english' if not set

# Set the output PDF file name based on the language flag
my $output_name = "memoir_$languageflag";

# pdflatex command with the language flag and output file name
$pdflatex = "pdflatex -synctex=1 -output-directory=$out_dir -jobname=$output_name \"\\newcommand{\\languageflag}{$languageflag}\\input{%S}\"";

$log_file = "$output_name.log";

# Define a subroutine to force rebuild
sub force_rebuild {
    open my $fh, '>', "$out_dir/.languageflag";
    print $fh $languageflag;
    close $fh;
    return 0;
}

# Add the dummy file as a custom dependency for the rebuild process
add_cus_dep('tex', 'force_rebuild', 0, 'force_rebuild');