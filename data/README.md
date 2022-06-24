# Model training data derived from passive acoustic recordings

A training set of spectrograms of fish calls was created based on annotations of fish sounds in passive acoustic recordings by a hydrophone were provided by Jim Locascio, Max Fullmer, and volunteers from the [Mote Marine Laboratory & Aquarium](https://mote.org).

The dataset contained here `labeled-spec-samples.tar.gz` was extracted from >1 TB archive of passive acoustic data.

## Dataset Processing

The raw data was reorganized with standardized names.  The provided annotations (`mote-samples.csv` derived from individual annotation files in `acoustic-data-annotations`) were then used to create a subset of audio files that contained calls.  That subset of audio files were then
used to generate spectrograms (`create_spectrograms.py`) that make up the training set.

## Dataset Labels

| Call Index | Description |
|------------|-------------|
|    0  |   Background noise (no fish vocalizations) |
|    1  |   Black grouper 1 |
|    2  |   Black grouper 2 |
|    3  |   Black grouper grunt |
|    4  |   Black grouper spawning rush |
|    5  |   Black grouper chorus < 50% of file |
|    6  |   Black grouper chrous > 50% of file |
|    8  |   Unidentified sound type |
|    9  |   Red grouper 1 |
|    10 |   Red grouper 2 |
|    17 |   Red hind 1 |
|    18 |   Red hind 2 |
|    19 |   Red hind 3 |
|    25 |   Goliath grouper 1 |
|    27 |   Multi-phase goliath grouper |
|    28 |   Sea trout chorus |
|    29 |   Silver perch call |

## Annotation data

The annotation files and notes related to that processes are located in the `acoustic-data-annotations` directory.  The file `mote-samples.csv`
was used to generate the training set.  `other-sampels.csv` included files from Toshiba hydrophones that were excluded only due to time constraints.
