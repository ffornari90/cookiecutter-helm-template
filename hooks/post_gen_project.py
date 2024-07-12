import subprocess
import yaml
import os

# Use the provided dep_chart_name, dep_chart_version, and dep_chart_repository
dep_chart_name = "{{cookiecutter.dep_chart_name}}"
dep_chart_version = "{{cookiecutter.dep_chart_version}}"
dep_chart_repository = "{{cookiecutter.dep_chart_repository}}"

# Define the path to the values.yaml file in your template using chart_name
values_yaml_path = os.path.join("{{cookiecutter.chart_name}}", "values.yaml")

# Function to run a Helm command and return the output
def run_helm_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    if result.returncode != 0:
        print(f"Error running Helm command: {result.stderr}")
        return None
    return result.stdout

# Function to populate values from Helm chart to values.yaml
def populate_values_from_helm_chart():
    if not dep_chart_name:
        print("No dependency chart specified. Skipping value population.")
        return

    # Check if Helm is available
    if run_helm_command("helm version --short") is None:
        print("Helm not found or not working. Please make sure Helm is installed and configured correctly.")
        return

    # Use Helm to get the values from the chart repository
    helm_command = f"helm show values {dep_chart_name} --repo {dep_chart_repository} --version {dep_chart_version}"
    helm_values = run_helm_command(helm_command)
    
    if helm_values is None:
        print(f"Failed to fetch values for chart {dep_chart_name} from repository {dep_chart_repository}")
        return

    # Load the Helm values into a Python dictionary
    try:
        helm_values_dict = yaml.safe_load(helm_values)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML from Helm values: {e}")
        return

    # Load existing values.yaml content
    try:
        with open(values_yaml_path, "r") as values_file:
            existing_values = yaml.safe_load(values_file)
    except FileNotFoundError:
        existing_values = {}
    except yaml.YAMLError as e:
        print(f"Error parsing existing values.yaml: {e}")
        return

    # Merge the Helm values with existing values
    existing_values[dep_chart_name] = helm_values_dict

    # Write the modified values to the values.yaml file
    try:
        with open(values_yaml_path, "w") as values_file:
            yaml.dump(existing_values, values_file, default_flow_style=False)
        print(f"Values populated from Helm chart to {values_yaml_path}")
    except IOError as e:
        print(f"Error writing to {values_yaml_path}: {e}")

if __name__ == "__main__":
    populate_values_from_helm_chart()
