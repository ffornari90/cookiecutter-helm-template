import os
import yaml

def update_values_yaml():
    values_file_path = os.path.join("{{ cookiecutter.chart_name }}", "values.yaml")
    
    with open(values_file_path, 'r') as file:
        values = yaml.safe_load(file)

    # Always keep all resource types, but as empty lists
    resource_types = ['deployments', 'services', 'ingresses', 'configMaps', 'databases', 'statefulSets', 'daemonSets', 'jobs', 'cronJobs']
    
    for resource_type in resource_types:
        if resource_type not in values:
            values[resource_type] = []

    # Remove dependency chart section if not needed
    if "{{ cookiecutter.need_dep_chart }}" == "no" and "{{ cookiecutter.dep_chart_name }}" in values:
        del values["{{ cookiecutter.dep_chart_name }}"]

    with open(values_file_path, 'w') as file:
        yaml.dump(values, file, default_flow_style=False)

if __name__ == "__main__":
    update_values_yaml()
