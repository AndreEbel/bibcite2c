from nbconvert.preprocessors import *
import re
import sys
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


class BibTexPreprocessor(Preprocessor):

    def create_bibentry(self, refkey, reference):
        """
        returns a dict with a bibtex-entry from cite2c reference data.
        currently three common reference types are implemented: articles, books and chapter of books.
        Parameters
        ----------
        refkey: str
            Zotero/Cite2c key of references
        reference: dictionary
            Dictonary with cite2c reference data as taken from cite2c JSON metadata
        """
        entry = {}

        entry['ID']=refkey
        if (reference["type"] == "article-journal"):
            entry['ENTRYTYPE']  = "article"
        elif (reference["type"] == "book"):
            entry['ENTRYTYPE']  = "book"
        elif (reference["type"] == "chapter"):
            entry['ENTRYTYPE']  = "inbook"
        elif (reference["type"] == "paper-conference"):
            entry['ENTRYTYPE']  = "inproceedings"
        else:
            # default type is misc!
            entry['ENTRYTYPE']  = "misc"
            print("Warning: Unknown type of reference "+refkey)

        if ("author" in reference):
            l = len(reference['author'])
            # if l > 1:
            authors = ''
            for i in range(l-1): 
                author=reference['author'][i]
                authors+=author['given']+' '+author['family']+ ' and '
            author=reference['author'][-1]
            authors+=author['given']+' '+author['family']
            entry['author']=authors
        else:
            print("Warning: No author(s) of reference " + refkey)

        if ("title" in reference):
            if reference["type"] == "chapter":
                entry['chapter']=reference['title']
            else:
                entry['title']=reference['title']
        else:
            print("Warning: No title of reference " + refkey)
            
        if ("container-title" in reference):
            if reference["type"] == "chapter":
                entry['title']=reference["container-title"]
            if reference["type"] == "paper-conference":
                entry['booktitle']=reference["container-title"]
            else:
                entry['journal']=reference["container-title"]

        if ("issued" in reference):
            entry['year'] = str(reference["issued"]["year"])
        if ("publisher" in reference):
            entry["publisher"] =reference["publisher"] 
        if ("page" in reference):
            entry['pages'] = reference["page"]
        if ("volume" in reference):
            entry['volume'] = reference["volume"]
        if ("issue" in reference):
            entry['issue'] = reference["issue"]
        if ("DOI" in reference):
            entry['doi'] = reference["DOI"]
        ## remove URL because it is often wrong and makes bibliography ugly
        #if ("URL" in reference):
        #    entry['url'] = reference["URL"]
        # print(entry)
        
        ## replace the & by \& so it appears properly after pdf converting and does not make pdflatex crash...
        for key in entry:
            s = entry[key]
            entry[key] = s.replace('&', '\&')
        return entry

    def create_bibfile(self, filename):
        """
        creates .bib with references from cite2c data in .ipynb JSON metadata using bibtexparser
        references must be places in self.references beforehand
        Parameters
        ----------
        filename: str
            filename in which the bibtex entries are saved
        """
        db = BibDatabase()
        db.entries  = []
        for r in self.references:
            if (sys.version_info > (3, 0)):
                db.entries.append(self.create_bibentry(r, self.references[r]))
            else:
                print('dont know what to do for sys.version_info <3')
        writer = BibTexWriter()
        with open(filename, 'w', encoding="utf-8") as bibfile:
            bibfile.write(writer.write(db))

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply on each notebook.
        Must return modified nb, resources.
        If you wish to apply your preprocessing to each cell, you might want
        to override preprocess_cell method instead.
        Parameters
        ----------
        nb : NotebookNode
            Notebook being converted
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        """
        # debugging: 
        # print('output extensions',resources["output_extension"])

        if not "cite2c" in nb["metadata"]:
            print ("Did not find cite2c metadata")
            return nb, resources
        if not "citations" in nb["metadata"]["cite2c"]:
            print ("Did not find cite2c metadata")
            return nb, resources

        self.references = nb["metadata"]["cite2c"]["citations"]
        bibfile =resources["unique_key"]+".bib"
        print('filename',bibfile)
        self.create_bibfile(bibfile)

        for index, cell in enumerate(nb.cells):
            nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
        return nb, resources

    def preprocess_cell(self, cell, resources, index):
        """
        Preprocess cell

        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being processed
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        cell_index : int
            Index of the cell being processed (see base.py)
        """
        if cell.cell_type == "markdown":
            replaced = None
            cell_code = "<div class=\"cite2c-biblio\"></div>"
            if cell_code in cell.source:
                new_cell_code = r'\\renewcommand\\refname{} \n'
                new_cell_code += r'\\bibliographystyle{unsrt} \n'
                new_cell_code += r"\\bibliography{"
                new_cell_code += resources["unique_key"]+r"}"
                
                replaced = re.sub(cell_code, new_cell_code, cell.source)
                # debugging
                # print('new cell code',new_cell_code )
            if replaced:
                cell.source = replaced
        return cell, resources
