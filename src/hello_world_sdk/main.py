import os

from azureml.core import Run
from func_to_script import script


@script
def log_greeting_to_azure_ml(greeting: str = 'Hello'):

    run = Run.get_context()

    # Tags are shown as properties of the job in the Azure ML dashboard. Run once.
    tags = {"greeting": greeting}
    run.set_tags(tags)

    # If you log metrics with same key multiple times, you get a plot in Azure ML
    run.log('answer', 42)

    print(f'{greeting}, World')


if __name__ == "__main__":
    log_greeting_to_azure_ml()