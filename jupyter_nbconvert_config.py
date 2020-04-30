c = get_config()

# The notebook you want to export
ntb = 'Untitled.ipynb'
# Exporting your notebook to pdf
c.NbConvertApp.notebooks = [ntb]
c.Exporter.preprocessors = [ 'bibcite2c.BibTexPreprocessor', 'pre_pymarkdown.PyMarkdownPreprocessor' ]
c.NbConvertApp.export_format = 'pdf'
# Extra parameters to remove the code cells (equivalent to --no-input)
c.TemplateExporter.exclude_output_prompt = True 
c.TemplateExporter.exclude_input = True 
# Template used
c.Exporter.template_file = 'classic'
