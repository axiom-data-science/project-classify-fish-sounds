# Fish Sound Detector

This repo is a collection of data, a Python library to work with Raven annotation files and generate spectrograms, and a model to detect
the vocalization of fish sounds from spectrograms generated from hydrophones as part of a collaboration between [Mote Marine Laboratory & Aquarium](https://mote.org), [Southeast Coastal Ocean Observing Regional Association](https://secoora.org), and [Axiom Data Science](https://axiomdatascience.com).

## Components

### Data

Included in the repo is a training set of spectrograms created from an annotated dataset of fish vocalizations labeled by domain experts and volunteers.
The provided annotation files are located in `data/acoustic-data-annotations` which were summarized in `data/acoustic-data-annotations/mote-samples.csv`.  See `data/README.md` for more information.

### Helper scripts / library

A Python package composed of various helpful scripts was created to reorganize and standardize the provided raw data and to generate training sets from which detector models could be trained.  The package can be installed via `pip`, e.g.

```bash
src/acoustic-tools> pip install -e .
```

### Notebooks

A Jupyter notebook `train-resetnet101-fastai.ipynb` is included which demonstrates how to train a neural network (ResNet101 implemented in fast.ai in the
example) to detect fish sounds using the provided labeled data.  The model has an accuracy of ~0.875 when training for 25 epochs using the selected
subset of annotated data that both undersamples classes with many examples and oversamples classess with few examples.

### Models

The model created in the notebook `train-resetnet101-fastai.ipynb` is saved in `models` and available from [Huggingface Hub](https://huggingface.co/axds/classify-fish-sounds).

### Demo

A running demo of the model is available on [Huggingface Spaces](https://huggingface.co/spaces/axds/classify-fish-sounds).
