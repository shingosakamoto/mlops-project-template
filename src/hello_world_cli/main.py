import os

import mlflow
from func_to_script import script


@script
def log_greeting_to_azure_ml(greeting: str = 'Hello'):
    # "MLFLOW_TRACKING_URI" is set-up when running inside an Azure ML Job
    # This command only needs to run once
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

    # Tags are shown as properties of the job in the Azure ML dashboard. Run once.
    tags = {"greeting": greeting}
    mlflow.set_tags(tags)

    # If you log metrics with same key multiple times, you get a plot in Azure ML
    metrics = {"answer": 42}
    mlflow.log_metrics(metrics)

    print(f'{greeting}, World')


if __name__ == "__main__":
    log_greeting_to_azure_ml()