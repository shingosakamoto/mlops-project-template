FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime

RUN apt-get update && apt-get install -y gcc ffmpeg libsm6 libxext6  -y

# Install pip dependencies
RUN pip install 'azureml-mlflow==1.39.0.post1' \
                'mlflow-skinny==1.24.0' \
                'pytorch-accelerated[examples]==0.1.26' \