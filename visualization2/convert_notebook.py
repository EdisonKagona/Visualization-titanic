# convert_notebook.py
import os
from nbconvert import ScriptExporter
from nbformat import read

def convert_notebook(notebook_path, output_path):
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = read(notebook_file, as_version=4)

    # Create an exporter
    exporter = ScriptExporter()

    # Export the notebook content to a Python script
    script, _ = exporter.from_notebook_node(notebook_content)

    # Write the script to the output file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(script)

if __name__ == "__main__":
    notebook_path = "visual2.ipynb"
    output_path = "visual2.py"
    convert_notebook(notebook_path, output_path)
