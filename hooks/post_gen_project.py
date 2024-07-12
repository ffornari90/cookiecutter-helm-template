import json

def main():
    # Load the initial context
    context = json.loads('{{ cookiecutter | jsonify }}')

    # Conditional logic for dependency chart
    if context['need_dep_chart'] == 'yes':
        context['dep_chart_name'] = input("Name of the dependency chart: ").strip()
        context['dep_chart_version'] = input("Version of the dependency chart: ").strip()
        context['dep_chart_repository'] = input("Repository of the dependency chart: ").strip()
    else:
        context['dep_chart_name'] = ""
        context['dep_chart_version'] = ""
        context['dep_chart_repository'] = ""

    # Conditional logic for deployment
    if context['include_deployment'] == 'yes':
        context['deployment_image_repo'] = input("Docker image repository for the deployment: ").strip()
        context['deployment_image_tag'] = input("Docker image tag for the deployment: ").strip()
    else:
        context['deployment_image_repo'] = ""
        context['deployment_image_tag'] = ""

    # Save the updated context to a file
    with open('cookiecutter_context.json', 'w') as f:
        json.dump(context, f)

