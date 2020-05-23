# -*- coding: utf-8 -*-
"""
Nbconvert preprocessor for the display correctly 
subscript and supersccript in text
"""

import re

from nbconvert.preprocessors import Preprocessor


class PyMarkdownPreprocessor(Preprocessor):
    """
    :mod:`nbconvert` Preprocessor for the python-markdown nbextension.

    This :class:`~nbconvert.preprocessors.Preprocessor` replaces kernel code in
    markdown cells with the results stored in the cell metadata.
    """

    def replace_superscript(self, source):
        """
        Replace <sup>variable</sup> with \textsuperscript{value}
        """
        pattern = '<sup>(.*?)</sup>'
        try:
            match = re.findall(pattern, source)
            replaced = source
            for i in range(len(match)):
                latex = r'\\textsuperscript{' + match[i] + r'}'
                replaced = re.sub(pattern, latex, replaced, count =1)
        except : #TypeError:
            replaced = source
        return replaced
    
    def replace_subscript(self, source):
        """
        Replace <sub>variable</sub> with \textsubscript{value}
        """
        pattern = '<sub>(.*?)</sub>'
        try:
            match = re.findall(pattern, source)
            replaced = source
            for i in range(len(match)):
                latex = r'\\textsubscript{' + match[i] + r'}'
                replaced = re.sub('<sub>(.*)</sub>', latex, replaced, count =1)
        except : #TypeError:
            replaced = source
        return replaced

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
            cell.source = self.replace_subscript(cell.source)
            cell.source = self.replace_superscript(cell.source)
        return cell, resources