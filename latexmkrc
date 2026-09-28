$pdf_mode = 5;
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$bibtex_use = 2;
$biber = 'biber %O %B';
$max_repeat = 5;

@generated_exts = (@generated_exts, 'bbl', 'bcf', 'blg', 'run.xml', 'synctex.gz');
