#!python
# Push a model to huggingface
# You must first login via `huggingface-cli`
import click
import logging
from pathlib import Path

import fastai.vision.all as fai_vision
from huggingface_hub import push_to_hub_fastai


@click.command()
@click.argument("path_to_serialized_model", type=click.Path(exists=True))
@click.argument("repo_id", type=click.STRING)
def main(path_to_serialized_model: Path, repo_id: str):
    learner = fai_vision.load_learner(path_to_serialized_model)
    logging.info("Pushing {path_to_serialized_model} to {repo_id}")
    push_to_hub_fastai(learner=learner, repo_id=repo_id)


if __name__ == "__main__":
    main()
