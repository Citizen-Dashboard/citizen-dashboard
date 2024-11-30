from kubernetes import client, config
from kubernetes.client import V1Job, V1JobSpec, V1ObjectMeta, V1PodTemplateSpec, V1PodSpec, V1Container, V1EnvFromSource, V1SecretEnvSource, V1LocalObjectReference
import argparse
import datetime
import time

def create_data_fetcher_job(from_date: str, to_date: str, job_name: str = None):
    if not job_name:
        job_name = f"data-fetcher-manual-job-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Define the container
    container = V1Container(
        name="data-fetcher",
        image="ghcr.io/citizen-dashboard/data-fetcher:latest",
        image_pull_policy="IfNotPresent",
        command=["poetry", "run", "python", "app/main.py"],
        args=[
            f"--from-date={from_date}",
            f"--to-date={to_date}"
        ],
        env_from=[
            V1EnvFromSource(
                secret_ref=V1SecretEnvSource(
                    name="ghcr-secret"
                )
            )
        ]
    )
    
    # Define the pod template
    template = V1PodTemplateSpec(
        metadata=V1ObjectMeta(labels={"app": "citizen-dashboard", "component": "data-fetcher"}),
        spec=V1PodSpec(
            restart_policy="OnFailure",
            containers=[container],
            image_pull_secrets=[V1LocalObjectReference(name="ghcr-secret")]
        )
    )
    
    # Define the job spec
    job_spec = V1JobSpec(
        template=template
    )
    
    # Create the job object
    job = V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=V1ObjectMeta(name=job_name),
        spec=job_spec
    )
    
    return job

def submit_job(job: V1Job):
    batch_v1 = client.BatchV1Api()
    try:
        response = batch_v1.create_namespaced_job(
            namespace="default",  # Replace with your namespace
            body=job
        )
        print(f"Job created. Name: {response.metadata.name}")
    except client.ApiException as e:
        print(f"Exception when creating job: {e}")

def monitor_job(job_name):
    batch_v1 = client.BatchV1Api()
    try:
        while True:
            job = batch_v1.read_namespaced_job(name=job_name, namespace="default")
            if job.status.succeeded is not None and job.status.succeeded >= 1:
                print(f"Job {job_name} completed successfully.")
                break
            elif job.status.failed is not None and job.status.failed >= 1:
                print(f"Job {job_name} failed.")
                break
            else:
                print(f"Job {job_name} is still running...")
            time.sleep(5)
    except client.ApiException as e:
        print(f"Exception when monitoring job: {e}")

def main():
    config.load_kube_config()  # Or config.load_incluster_config()

    parser = argparse.ArgumentParser(description='Run Data Fetcher Job')
    parser.add_argument('--from-date', required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--to-date', required=True, help='End date in YYYY-MM-DD format')
    args = parser.parse_args()

    job = create_data_fetcher_job(args.from_date, args.to_date)
    submit_job(job)
    monitor_job(job.metadata.name)

if __name__ == "__main__":
    main()
