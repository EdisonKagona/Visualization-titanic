# auto_update_script.py
import time
import os
from convert_notebook import convert_notebook

def monitor_notebook_changes(notebook_path, output_path):
    # Get the initial modification time of the notebook
    last_modified_time = os.path.getmtime(notebook_path)

    while True:
        # Check for changes every 2 seconds
        time.sleep(2)

        # Get the current modification time of the notebook
        current_modified_time = os.path.getmtime(notebook_path)

        # If the notebook has been modified, update the script
        if current_modified_time > last_modified_time:
            last_modified_time = current_modified_time
            convert_notebook(notebook_path, output_path)
            print(f"Updated {output_path} at {time.ctime()}")

if __name__ == "__main__":
    notebook_path = "visual1.ipynb"
    output_path = "visual1.py"
    monitor_notebook_changes(notebook_path, output_path)
