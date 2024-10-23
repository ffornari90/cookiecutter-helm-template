import json

def prompt_user(question, default=None):
    """ Helper function to prompt the user and return the input or default value. """
    response = input(f"{question} {'(' + default + ')' if default else ''}: ").strip()
    return response if response else default

def main():
    # Load the initial context
    context_str = r"""
    {{ cookiecutter | jsonify }}
    """
    context = json.loads(context_str)

    # Conditional logic for dependency chart
    if context['need_dep_chart'] == 'yes':
        context['dep_chart_name'] = prompt_user("Name of the dependency chart", "dependency-chart")
        context['dep_chart_version'] = prompt_user("Version of the dependency chart", "0.1.0")
        context['dep_chart_repository'] = prompt_user("Repository of the dependency chart", "https://charts.example.com")
    else:
        context['dep_chart_name'] = ""
        context['dep_chart_version'] = ""
        context['dep_chart_repository'] = ""

    # Conditional logic for deployment
    if context['include_deployment'] == 'yes':
        context['deployment_image_repo'] = prompt_user("Docker image repository for the deployment", "nginx")
        context['deployment_image_tag'] = prompt_user("Docker image tag for the deployment", "latest")
    else:
        context['deployment_image_repo'] = ""
        context['deployment_image_tag'] = ""

    # Save the updated context to a file for debugging purposes (optional)
    with open('cookiecutter_context.json', 'w') as f:
        json.dump(context, f, indent=4)

if __name__ == "__main__":
    main()
