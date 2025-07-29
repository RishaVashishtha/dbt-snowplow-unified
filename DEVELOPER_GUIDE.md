
# Developer Guide: Automated dbt Project Structure Generator

## Overview
This guide explains how the `automate.py` script streamlines the creation of a dbt project structure for individual customer that facilitate the customization process. The script uses a customer-specific JSON configuration and a template `dbt_project.yml` to generate a fully customized dbt project folder, including all required subfolders and a tailored configuration file.

---

## How It Works

### 1. Inputs
- **JSON config file**: Data in JSON format that is specific to the individual customer (e.g., name, app IDs, tracking options).
- **Template YAML**: `dbt_project_template.yml` in the script directory, used as the base (template) for the generated `dbt_project.yml`.
- **Destination directory**: Where the new customer specific folder will be created.

### 2. Execution
Run the script from the command line:

```bash
python automate.py <customer_config.json> <destination_base_dir>
# Example:
python automate.py Backpacker_Connect.json /path/to/dbt-snowplow-unified
```

### 3. Script Actions
- Loads the JSON config for the customer.
- Creates a new folder for the customer (e.g., `backpacker_connect`) in the destination directory.
- Creates standard dbt subfolders inside the customer folder (models, macros, docs, etc).
- Loads the template YAML, merges in customer-specific overrides, and writes a customized `dbt_project.yml` into the new customer folder.

---

## Key Functions

- **`load_json_config(file_path)`**
  - Loads and parses the customer’s JSON config.
- **`create_customer_project_dir(customer_name, base_dir)`**
  - Creates a new directory for the customer, formatted as lowercase with underscores.
- **`create_dbt_project_structure(project_dir)`**
  - Creates all standard dbt subfolders inside the customer directory.
- **`recursive_merge(original, overrides)`**
  - Recursively merges the customer-specific overrides into the template YAML.
- **`create_and_override_dbt_project_yml(template_path, dest_project_dir, overrides)`**
  - Loads the template YAML, applies overrides, and writes the result as `dbt_project.yml` in the customer folder.

---

## Customization Logic
The script reads variables like `customer_name`, `app_ids`, and tracking flags from the JSON. These are injected into the `vars` section of the generated `dbt_project.yml`This allows each customer to have its own configuration, optimized for its requirements (e.g., enabling/disabling web/mobile tracking, setting session windows, etc)..However the `version`,`config-version`,`require-dbt-version` are taken from the refernced `dbt_project_template`.

---

## Error Handling
- **FileNotFoundError**: Prints if the actual JSON file is missing.
- **JSONDecodeError**: Alerts if the JSON config is invalid.
- **KeyError**: Alerts if required keys (like `customer_name`) are missing in the JSON and exits the script.

---

## Adding a New customer
1. Create a JSON config for the customer can be refernced from  `Backpacker_connect.json`,`LastMinute_Deals.json` etc.
2. Run the script with the new JSON and your dbt project base directory.
3. Check the output folder for the new customer’s customized dbt project.

---

## Template Location
The script expects `dbt_project_template.yml` to be in the same directory as `automate.py`. If you want to use a different template, update the `template_path` logic in the script.