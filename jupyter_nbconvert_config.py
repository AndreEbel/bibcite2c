c = get_config()

# It is assumed there is only one notebook in the folder
c.NbConvertApp.notebooks = ['*.ipynb']
# Preprocessors 
c.Exporter.preprocessors = ['bibcite2c.BibTexPreprocessor', 
                            'pre_pymarkdown.PyMarkdownPreprocessor', 
                            'pre_subsupmarkdown.PyMarkdownPreprocessor']
c.NbConvertApp.export_format = 'pdf'
# Extra parameters to remove the code cells (equivalent to --no-input)
c.TemplateExporter.exclude_output_prompt = True 
c.TemplateExporter.exclude_input = True 
# Template used
c.Exporter.template_file = 'classic'
