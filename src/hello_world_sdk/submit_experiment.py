from azureml.core import Workspace, Experiment, Environment, ScriptRunConfig

def main():

    ws = Workspace.from_config()
    experiment = Experiment(workspace=ws, name='hello-world-sdk')

    env = Environment.get(ws, name='hello-world-sdk')

    config = ScriptRunConfig(source_directory='.',
                             script='main.py',
                             compute_target='cpu-cluster',
                             environment=env)

    run = experiment.submit(config)
    aml_url = run.get_portal_url()
    print(aml_url)

if __name__ == '__main__':
    main()