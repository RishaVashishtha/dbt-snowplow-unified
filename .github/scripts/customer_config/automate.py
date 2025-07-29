import json
import sys
import os
import shutil
import yaml

# Read and parse a JSON file to extract the customer name and create a project directory structure for dbt.
def load_json_config(file_path):
    """Loads and returns JSON data from the given file path."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


# Create the customer folder based on the customer name from the JSON file
def create_customer_project_dir(customer_name, base_dir: str):
    # Convert to lowercase and replace spaces with underscores
    folder_name = customer_name.lower().replace(' ', '_')
    path = os.path.join(base_dir, folder_name)
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {folder_name}")
    return path

# Create standard dbt project structure
def create_dbt_project_structure(project_dir: str):
    """Create standard dbt folders and starter files."""
    # Define standard dbt subfolders
    subfolders = ['assets', 'docs/markdown', 'macros', 'models/base/manifest','models/base/scratch','models/sessions/scratch','models/sessions/manifest','models/users/scratch','models/users/manifest','models/views/scratch','models/views/manifest','seeds', 'tests']
    for subfolder in subfolders:
        os.makedirs(os.path.join(project_dir, subfolder), exist_ok=True)
        print(f"Created subfolder: {os.path.join(project_dir, subfolder)}")

def recursive_merge(original, overrides):
    for key, value in overrides.items():
        if isinstance(value, dict) and key in original and isinstance(original[key], dict):
            recursive_merge(original[key], value)
        else:
            original[key] = value


def create_and_override_dbt_project_yml(template_path, dest_project_dir, overrides: dict):
    """Copy the template dbt_project.yml and override specified values."""
    
    print(f"[DEBUG] create_and_override_dbt_project_yml will write to: {os.path.join(dest_project_dir, 'dbt_project.yml')}")
    # 1. Load template YAML
    with open(template_path, 'r') as f:
        yml_data = yaml.safe_load(f)

    recursive_merge(yml_data, overrides)
    # 3. Write the new YAML to the new location
    dest_path = os.path.join(dest_project_dir, 'dbt_project.yml')
    with open(dest_path, 'w') as f:
        yaml.dump(yml_data, f, sort_keys=False)
    print(f"Created customized dbt_project.yml at: {dest_path}")
    return dest_path
# result = load_json_config('Luxury_Stays.json')
# print (result)
def str_to_bool(val):
    return str(val).strip().lower() in ['yes', 'true', '1']

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <json_filename>")
        sys.exit(1)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"-----Script directory:----- {script_dir}")
    filename = sys.argv[1]
    if not os.path.isabs(filename):
        filename = os.path.join(script_dir, filename)
    filename = os.path.abspath(filename)

    dir_path = os.path.abspath(sys.argv[2])
    template_path = os.path.join(script_dir, 'dbt_project_template.yml')
    # //os.mkdir(filename)
    try:
        result = load_json_config(filename)
        print(result)
        print(f"-------Loaded JSON configuration from: {filename}")
        customer_name = result.get('brand_name')
        if not customer_name:
            raise KeyError("Missing 'brand_name' in JSON configuration.")
        project_dir = create_customer_project_dir(customer_name, dir_path) 
        create_dbt_project_structure(project_dir)
        # Create dbt_project.yml with overrides
        overrides = {
        'name': result.get('customer_name', '').lower().replace(' ', '_'),

        'vars': {
            'snowplow_unified': {
                'snowplow__app_id': result.get('app_ids', []),
                'snowplow__max_session_days': result.get('user_set_variables', {}).get('snowplow__max_session_days'),
                'snowplow__lookback_window_hours': result.get('user_set_variables', {}).get('snowplow__lookback_window_hours'),
                'snowplow__start_date': result.get('historical_data_since'),
                'snowplow__enable_web': str_to_bool(result.get('web_tracking', '')),
                'snowplow__enable_mobile': str_to_bool(result.get('mobile_tracking', '')),
            }
         },
        }
        template_path = os.path.join(script_dir, 'dbt_project_template.yml')  # Path to your template file
        print(f"**********Template path: {template_path}")
        
        print(f"Writing dbt_project.yml to: {os.path.join(project_dir, 'dbt_project.yml')}")
        
        create_and_override_dbt_project_yml(template_path, project_dir, overrides)
        
        print(f"+++++++++++Project directory created at: {project_dir}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON. {e}")
    except KeyError:
        print("Error: 'customer_name' missing from JSON.")
        # sys.exit(1)
