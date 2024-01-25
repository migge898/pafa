from kubernetes.client.rest import ApiException
from kubernetes import client, config

config.load_kube_config()

pod_name = "grafana-78977f78b6-t26qv"
try:
    api_instance = client.CoreV1Api()
    api_response = api_instance.read_namespaced_pod_log(name=pod_name, namespace='monitoring')
    print(api_response)
except ApiException as e:
    print('Found exception in reading the logs')