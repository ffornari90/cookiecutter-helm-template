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
            "name": context['chart_name'],
            "s3Secret": context['deployment_s3_secret'],
            "replicaCount": 1,
            "image": {
                "repository": context['deployment_image_repo'],
                "tag": context['deployment_image_tag'],
                "pullPolicy": "IfNotPresent",
                "pullSecret": context['deployment_image_secret']
            },
            "containerPort": 80
        }
        values['deployments'].append(deployment)

    # Update services section if 'include_service' is 'yes'
    if context.get('include_service') == 'yes':
        service = {
            "name": context['chart_name'],
            "type": context.get('service_type', 'ClusterIP'),
            "port": context.get('service_port', 80),
            "selector": context['chart_name'] if context['include_deployment'] == 'yes' else "app"
        }
        values['services'].append(service)

    # Update configmaps section if 'include_configmap' is 'yes'
    if context.get('include_configmap') == 'yes':
        configmap = {
            "name": context.get('configmap_name', 'example-config'),
            "data": {
                "APP_CONFIG": context.get('configmap_data', 'key1: value1\nkey2: value2')
            }
        }
        values['configMaps'].append(configmap)

    # Update cronjobs section if 'include_cronjob' is 'yes'
    if context.get('include_cronjob') == 'yes':
        cronjob = {
            "name": context.get('cronjob_name', 'example-cronjob'),
            "schedule": context.get('cronjob_schedule', '0 * * * *'),
            "image": {
                "repository": context.get('cronjob_image_repo', 'your-registry/example-cron-app'),
                "tag": context.get('cronjob_image_tag', 'latest')
            },
            "restartPolicy": "OnFailure"
        }
        values['cronJobs'].append(cronjob)

    # Update daemonsets section if 'include_daemonset' is 'yes'
    if context.get('include_daemonset') == 'yes':
        daemonset = {
            "name": context.get('daemonset_name', 'example-daemonset'),
            "image": {
                "repository": context.get('daemonset_image_repo', 'your-registry/example-daemon-app'),
                "tag": context.get('daemonset_image_tag', 'latest')
            }
        }
        values['daemonSets'].append(daemonset)

    # Update databases section if 'include_database' is 'yes'
    if context.get('include_database') == 'yes':
        database = {
            "name": context.get('database_name', 'example-db'),
            "dbName": context.get('database_db_name', 'example-db'),
            "psqlClusterName": context.get('database_psql_cluster', 'home-postgres-cluster'),
            "allowConnections": True
        }
        values['databases'].append(database)

    # Update ingresses section if 'include_ingress' is 'yes'
    if context.get('include_ingress') == 'yes':
        ingress = {
            "name": context.get('ingress_name', 'example-ingress'),
            "annotations": {
                "kubernetes.io/ingress.class": "nginx"
            },
            "host": context.get('ingress_host', 'chart-example.local'),
            "serviceName": context.get('service_name', 'example-service'),
            "servicePort": context.get('service_port', 80),
            "path": "/",
            "pathType": "Prefix",
            "tls": False,
            "tlsSecretName": context.get('tls_secret_name', 'chart-example-tls')
        }
        values['ingresses'].append(ingress)

    # Update jobs section if 'include_job' is 'yes'
    if context.get('include_job') == 'yes':
        job = {
            "name": context.get('job_name', 'example-job'),
            "image": {
                "repository": context.get('job_image_repo', 'your-registry/example-job-app'),
                "tag": context.get('job_image_tag', 'latest')
            },
            "restartPolicy": "OnFailure"
        }
        values['jobs'].append(job)

    # Update statefulsets section if 'include_statefulset' is 'yes'
    if context.get('include_statefulset') == 'yes':
        statefulset = {
            "name": context.get('statefulset_name', 'example-statefulset'),
            "serviceName": context.get('statefulset_service_name', 'example-statefulset-svc'),
            "replicaCount": 1,
            "image": {
                "repository": context.get('statefulset_image_repo', 'your-registry/example-stateful-app'),
                "tag": context.get('statefulset_image_tag', 'latest')
            }
        }
        values['statefulSets'].append(statefulset)

    # Update external_s3_secrets section if 'include_external_s3_secret' is 'yes'
    if context.get('include_external_s3_secret') == 'yes':
        external_s3_secret = {
            "name": context.get('external_s3_secret_name', 'example-external-s3-secret'),
            "target": {
                "name": context.get('k8s_s3_secret_name', 'example-kubernetes-s3-secret')
            },
            "data": [
                {
                    "secretKey": entry['secret_key'],
                    "remoteRef": {
                        "key": entry['vault_secret_key'],
                        "property": entry['vault_secret_property']
                    }
                } for entry in context.get('external_s3_secret_data', {"data":[{"secret_key": "example-key-1","vault_secret_key": "vault/secret/data/path-1","vault_secret_property": "secret-property-1"},{"secret_key": "example-key-2","vault_secret_key": "vault/secret/data/path-2","vault_secret_property": "secret-property-2"}]}).get('data')
            ]
        }
        values['externalS3Secrets'].append(external_s3_secret)

    # Update external_registry_secrets section if 'include_external_registry_secret' is 'yes'
    if context.get('include_external_registry_secret') == 'yes':
        external_registry_secret = {
            "name": context.get('external_registry_secret_name', 'example-external-registry-secret'),
            "target": {
                "name": context.get('k8s_registry_secret_name', 'example-kubernetes-registry-secret')
            },
            "data": [
                {
                    "secretKey": entry['secret_key'],
                    "remoteRef": {
                        "key": entry['vault_secret_key'],
                        "property": entry['vault_secret_property']
                    }
                } for entry in context.get('external_registry_secret_data', {"data":[{"secret_key": "example-key-1","vault_secret_key": "vault/secret/data/path-1","vault_secret_property": "secret-property-1"},{"secret_key": "example-key-2","vault_secret_key": "vault/secret/data/path-2","vault_secret_property": "secret-property-2"}]}).get('data')
            ]
        }
        values['externalRegistrySecrets'].append(external_registry_secret)

    # Update external_gitlab_secrets section if 'include_external_gitlab_secret' is 'yes'
    if context.get('include_external_gitlab_secret') == 'yes':
        external_gitlab_secret = {
            "name": context.get('external_gitlab_secret_name', 'example-external-gitlab-secret'),
            "target": {
                "name": context.get('k8s_gitlab_secret_name', 'example-kubernetes-gitlab-secret')
            },
            "data": [
                {
                    "secretKey": entry['secret_key'],
                    "remoteRef": {
                        "key": entry['vault_secret_key'],
                        "property": entry['vault_secret_property']
                    }
                } for entry in context.get('external_gitlab_secret_data', {"data":[{"secret_key": "example-key-1","vault_secret_key": "vault/secret/data/path-1","vault_secret_property": "secret-property-1"},{"secret_key": "example-key-2","vault_secret_key": "vault/secret/data/path-2","vault_secret_property": "secret-property-2"}]}).get('data')
            ]
        }
        values['externalGitlabSecrets'].append(external_gitlab_secret)

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
