import json
import sys
import os

def create_brand_project_dir(brand_name, base_dir: str):
    # Convert to lowercase and replace spaces with underscores
    folder_name = brand_name.lower().replace(' ', '_')
    path = os.path.join(base_dir, folder_name)
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {folder_name}")
    return path

# Create standard dbt project structure
def create_dbt_project_structure(project_dir: str):
    """Create standard dbt folders and starter files."""
    # Define standard dbt subfolders
    subfolders = ['models/staging', 'tests', 'macros', 'seeds', 'analyses']
    for subfolder in subfolders:
        os.makedirs(os.path.join(project_dir, subfolder), exist_ok=True)
        print(f"Created subfolder: {os.path.join(project_dir, subfolder)}")

def load_json_config(file_path):
    """Loads and returns JSON data from the given file path."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
# result = load_json_config('Luxury_Stays.json')
# print (result)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <json_filename>")
        sys.exit(1)
    filename = sys.argv[1]
    dir_path = sys.argv[2]

    # //os.mkdir(filename)
    try:
        result = load_json_config(filename)
        print(result)
        brand_name = result.get('brand_name')
        project_dir = create_brand_project_dir(brand_name, dir_path) 
        create_dbt_project_structure(project_dir)
        print(f"Project directory created at: {project_dir}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON. {e}")
    except KeyError:
        print("Error: 'brand_name' missing from JSON.")
        sys.exit(1)
