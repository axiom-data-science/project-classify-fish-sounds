# acoustic-tools

Tools used in development of the fish sound detector.

## Install

The package is installable via `pip`.  It is not published anywhere.

```bash
pip install -e .
```

## Scripts

Apart from the bash script to move data, the remaininig scripts are Python and have usage details provided if no arguments are provided.


1. `move-mote-data.sh`

- Used in reoranizing data transferred from Mote Lab to Axiom

2. `rename_training_set_files.py`

- Used to rename files and used in `move-mote-data.sh`

3. `write_annotation_file.py`

- Used to create a single annotation file to create training samples from annotation files saved in `data/acoustic-data-annotations`

4. `create_training_set.py`

- Used to create a training set of sample wav files given an annotation file created by `write_annotation_file.py`

5. `create_spectrograms.py`

- Used to create spectrograrms given a directory of wav files.

6. `push-model-to-hf.py`

- Used to push existing model to Huggingface Hub.