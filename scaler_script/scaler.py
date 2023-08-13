import sys
# import pprint
import logging
from kubernetes import client, config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scale_deployment(deployment_name, replica_count, namespace):
    try:
        # Load the in-cluster configuration
        config.load_incluster_config()

        # load the out-of-cluster configuration
        # config.load_kube_config()
        # pprint.pprint(config.list_kube_config_contexts())

        api_instance = client.AppsV1Api()

        # Fetch the current deployment
        deployment = api_instance.read_namespaced_deployment(
            name=deployment_name,
            namespace=namespace
        )

        # pprint.pprint(deployment)

        # Update the replica count
        deployment.spec.replicas = replica_count

        # Update the deployment
        response = api_instance.replace_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=deployment
        )
        
        logger.info(f"Deployment '{deployment_name}' in namespace '{namespace}' scaled to {replica_count} replicas.")    
    
    except Exception as e:
        logger.error(f"Error scaling deployment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 scaler.py deploymentName replicaCount [namespaceName]")
        sys.exit(1)

    deployment_name = sys.argv[1]
    replica_count = int(sys.argv[2])
    namespace = sys.argv[3] if len(sys.argv) == 4 else "default"

    try:
        scale_deployment(deployment_name, replica_count, namespace)
    except KeyboardInterrupt:
        logger.warning("Script execution interrupted.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")