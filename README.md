# bibcite2c
BibTexPreprocessor for exporting jupyter notebook containing [cite2c](https://github.com/takluyver/cite2c) citations to pdf using [nbconvert](https://github.com/jupyter/nbconvert).

The files are directly inspired from [jupyter-publication-scripts](https://github.com/schlaicha/jupyter-publication-scripts). The only change is that the bibtex file is generated from the notebook metadata using [bibtexparser](https://github.com/sciunto-org/python-bibtexparser).

## Step 0
Add citations and bibliography in your notebook using [cite2c](https://github.com/takluyver/cite2c) 

## Step 1
add bibcite2c.py and jupyter_nbconvert_config.py in your directory.

## Step 2
modify the ntb variable in jupyter_nbconvert_config.py with your actual jupyter notebook name (with extension).

## Step 2
run the following command in your notebook:   

!jupyter nbconvert   

## Just a last word 
Let's hope it may be useful to someone. 


