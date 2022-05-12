# taken from https://github.com/Chris-hughes10/pytorch-accelerated/blob/main/examples/train_mnist.py

import os

import mlflow
from pytorch_accelerated import Trainer
from pytorch_accelerated.callbacks import LogMetricsCallback, get_default_callbacks
from torch import nn, optim
from torch.utils.data import random_split
from torchvision import transforms
from torchvision.datasets import MNIST


class AzureMLLoggerCallback(LogMetricsCallback):
    def __init__(self):
        mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])

    def on_training_run_start(self, trainer, **kwargs):
        if trainer.run_config.is_world_process_zero:
            mlflow.set_tags(trainer.run_config.to_dict())

    def log_metrics(self, trainer, metrics):
        if trainer.run_config.is_world_process_zero:
            mlflow.log_metrics(metrics)


class MNISTModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.main = nn.Sequential(
            nn.Linear(in_features=784, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=64),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=10),
        )

    def forward(self, x):
        return self.main(x.view(x.shape[0], -1))


def main():
    dataset = MNIST(os.getcwd(), download=True, transform=transforms.ToTensor())
    train_dataset, validation_dataset, test_dataset = random_split(
        dataset, [50000, 5000, 5000]
    )
    model = MNISTModel()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    loss_func = nn.CrossEntropyLoss()

    trainer = Trainer(
        model,
        loss_func=loss_func,
        optimizer=optimizer,
        callbacks=(*get_default_callbacks(progress_bar=False),
                   AzureMLLoggerCallback)
    )

    trainer.train(
        train_dataset=train_dataset,
        eval_dataset=validation_dataset,
        num_epochs=2,
        per_device_batch_size=32,
    )

    trainer.evaluate(
        dataset=test_dataset,
        per_device_batch_size=64,
    )


if __name__ == "__main__":
    main()
