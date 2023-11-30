import os
from convert_notebook import convert_notebook

def update_dash_app():
    # Step 1: Update the notebook
    notebook_path = "visual2.ipynb"
    output_path = "visual2.py"
    convert_notebook(notebook_path, output_path)

    # Step 2: Run the Dash app
    os.system("python app.py")

if __name__ == "__main__":
    update_dash_app()
