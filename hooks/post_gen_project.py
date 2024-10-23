import json
import yaml

def update_values_yaml(context):
    """ Function to update the values.yaml file with the provided context. """
    # Load the existing values.yaml file
    with open('values.yaml', 'r') as file:
        values = yaml.safe_load(file)

    # Update deployments section if 'include_deployment' is 'yes'
    if context['include_deployment'] == 'yes':
        deployment = {
            "name": context['deployment_image_repo'].split('/')[-1],
            "replicaCount": 1,
            "image": {
                "repository": context['deployment_image_repo'],
                "tag": context['deployment_image_tag'],
                "pullPolicy": "IfNotPresent"
            },
            "containerPort": 80
        }
        values['deployments'].append(deployment)

    # If a dependency chart is needed, populate the chart information
    if context['need_dep_chart'] == 'yes':
        dep_chart = {
            context['dep_chart_name']: {
                "repository": context['dep_chart_repository'],
                "version": context['dep_chart_version']
            }
        }
        values.update(dep_chart)

    # Save the updated values.yaml file
    with open('values.yaml', 'w') as file:
        yaml.dump(values, file, default_flow_style=False)

def main():
    # Load the initial context
    context_str = r"""
    {{ cookiecutter | jsonify }}
    """
    context = json.loads(context_str)

    # Update the values.yaml file with the provided context
    update_values_yaml(context)

if __name__ == "__main__":
    main()
