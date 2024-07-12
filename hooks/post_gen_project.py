import os
import shutil

def remove_resource_files(resource_type):
    file_path = os.path.join("{{ cookiecutter.chart_name }}", "templates", f"{resource_type}.yaml")
    if os.path.exists(file_path):
        os.remove(file_path)

def process_additional_resources():
    additional_resources = "{{ cookiecutter.additional_resources }}".split(',')
    all_resources = ['databases', 'configmaps', 'statefulsets', 'daemonsets', 'jobs', 'cronjobs']
    
    for resource in all_resources:
        if resource not in additional_resources:
            remove_resource_files(resource)

def cleanup_unused_resources():
    setup_type = "{{ cookiecutter.setup_type }}"
    if setup_type == "default":
        process_additional_resources()
    elif setup_type == "custom":
        if "{{ cookiecutter.include_databases }}" == "no":
            remove_resource_files("database")
        if "{{ cookiecutter.include_deployments }}" == "no":
            remove_resource_files("deployment")
        if "{{ cookiecutter.include_services }}" == "no":
            remove_resource_files("service")
        if "{{ cookiecutter.include_ingresses }}" == "no":
            remove_resource_files("ingress")
        if "{{ cookiecutter.include_configmaps }}" == "no":
            remove_resource_files("configmap")
        if "{{ cookiecutter.include_statefulsets }}" == "no":
            remove_resource_files("statefulset")
        if "{{ cookiecutter.include_daemonsets }}" == "no":
            remove_resource_files("daemonset")
        if "{{ cookiecutter.include_jobs }}" == "no":
            remove_resource_files("job")
        if "{{ cookiecutter.include_cronjobs }}" == "no":
            remove_resource_files("cronjob")

if __name__ == "__main__":
    cleanup_unused_resources()
