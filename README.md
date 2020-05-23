# bibcite2c
BibTexPreprocessor for exporting jupyter notebook containing [cite2c](https://github.com/takluyver/cite2c) citations to pdf using [nbconvert](https://github.com/jupyter/nbconvert).

The files are directly inspired from [jupyter-publication-scripts](https://github.com/schlaicha/jupyter-publication-scripts). The only change is that the bibtex file is generated from the notebook metadata using [bibtexparser](https://github.com/sciunto-org/python-bibtexparser).

## Step 0
Add citations and bibliography in your notebook using [cite2c](https://github.com/takluyver/cite2c) 

## Step 1
Add the following files in your working directory: 
- bibcite2c.py for reference handling
- pre_subsupmarkdown.py for handling superscript and subscript during converting markdown to latex and then to pdf
- python-markdown [preprocessor](https://github.com/ipython-contrib/jupyter_contrib_nbextensions/blob/master/src/jupyter_contrib_nbextensions/nbconvert_support/pre_pymarkdown.py)
- jupyter_nbconvert_config.py 

## Step 2
Run the following command in your notebook:   

!jupyter nbconvert   

## Just a last word 
Let's hope it may be useful to someone. 

Only works for pdf export.


