# automation_script.py
import os
from convert_notebook import convert_notebook

def run_dash_app(dash_script_path):
    os.system(f"python {dash_script_path}")

if __name__ == "__main__":
    notebook_path = "visual1.ipynb"
    output_path = "visual1.py"
    dash_script_path = "app.py"
    
    convert_notebook(notebook_path, output_path)
    run_dash_app(dash_script_path)
