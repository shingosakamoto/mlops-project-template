from azureml.core import Environment, Workspace
from func_to_script import script


@script
def main(environment_name: str = 'myenv',
         conda_file_path: str = 'conda_requirements.yaml',
         force_docker_build: bool = False):

    ws = Workspace.from_config()
    print(f"About to register environment {environment_name} to workspace: {ws}")
    env = Environment.from_conda_specification(name=environment_name, file_path=conda_file_path)
    env.register(workspace=ws)

    if force_docker_build:
        print("Building environment")
        build = env.build(ws)
        build.wait_for_completion(show_output=True)

if __name__ == '__main__':
    main()