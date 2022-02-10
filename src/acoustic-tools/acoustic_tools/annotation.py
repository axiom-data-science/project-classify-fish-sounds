"""Raven annotation parser."""
import datetime
import logging
from pathlib import Path

import numpy as np
import pandas as pd


# unable to use "usecols" kwarg for read_csv
DROP_COLS = [
    'Selection',
    'View',
    'Channel',
    'Notes',
    'Low Freq (Hz)',
]

RENAME_COLS = {
    'Begin File': 'file',
    'Delta Time (s)': 'call_length',
    'File Offset (s)': 'start_time',
    'call variant': 'call_variant',
    'level': 'signal_level',
    'calls overlap': 'call_overlap',
    # not a typo, both column names exist
    'call cutoff @ end?': 'call_cutoff',
    'call cutoff @ end': 'call_cutoff',
    'High Freq (Hz)': 'high_freq'
}

# directories containing annotation files
# correspond to filename prefixes in move-mote-data.sh
FILE_NAMES = [
    'bermuda',
    'd9-sarasota',
    'exxon-template-tower'
    'goliath-jupiter-gulf',
    'jupiter',
    'port-manatee',
    'rileys-hump',
    'usf-glider'
]


def read_annotation_file(
    annotation: Path,
    drop_cols: list = DROP_COLS,
    rename_cols: dict = RENAME_COLS
) -> pd.DataFrame:
    """Given path to BlackGrouper annotation file, return annotations as a DataFrame.

    Parameters
    ----------
    annotation_file: Path
        Path to annotation file
    new_name: str
        Prefix of name of file (needs to match organization in `reorg` dir of wav files)

    Returns
    -------
    annotation: pd.DataFrame
        DataFrame of selected annotation data

    Notes
    -----
    - This function drops columns of annotated data not required for development of Black Grouper classifier.
    - Bool values for `calls overlap` and `call cutoff @ end?` determined from metadata described in
      https://docs.google.com/spreadsheets/d/16NzrodSu2MhiBPzKBrQKCi923lWDKvzT/edit#gid=616126176
        - Call variants: 6 variants
        - Level: 3 levels of relative amplitude (1: high, 2: medium, 3: low)
        - Overlap: Do calls overlap (1: yes, 2: no)
        - Cutoff: Are calls cutoff at end (1: yes, 2: no)
    """

    df = (pd.read_csv(
        annotation,
        sep='\t',
    )
        .drop(columns=drop_cols)
        .rename(columns=rename_cols)
        .dropna()
    )
    # Drop rows with wavform, keep only spec (some files essentially duplicate the annotated calls)
    # File will be of form:
    # HEADER ...
    # ix ... Waveform 1 ... LENGTH_1
    # xi+2 ... Spectrogram 1 ... LENGTH_1
    if df.iloc[0].call_length == df.iloc[1].call_length:
        df = df.drop(index=np.arange(0, len(df), 2))

    df['signal_level'] = df['signal_level'].astype(int)
    # 1 == True
    # 2 == False
    df['call_overlap'] = df['call_overlap'].apply(lambda x: bool(x % 2))
    df['call_cutoff'] = df['call_cutoff'].apply(lambda x: bool(x % 2))

    # Some files will have two 'call_cutoff' columns due to the '?' added in some column labels.
    # - So, we remove call_cutff.1 from the dataframe.
    if 'call_cutoff.1' in df.columns:
        df = df.drop(columns=['call_cutoff.1'])

    # Some have column name "End Times (s)" - drop it.
    bad_column = 'End Time (s)'
    if bad_column in df.columns:
        df = df.drop(columns=[bad_column])

    new_names = []
    # None Toshiba files
    if 'DSG' in df['file'].iloc[0]:
        # Files names have spaces in them, but were removed
        df['file'] = df['file'].apply(lambda x: x.replace(' ', ''))

        # File names have inconsistent formatting, so we'll rename them:
        # YYYY-MM-DDTHHMMSS.wav
        files = df['file']
        for file in files:
            # e.g. 748.DSG_RAWD_HMS_19_0_0__DMY_25_7_16.wav
            # pull out empty ('') segments, exist because of different number of '_' in filename
            segments = [seg for seg in file.split('.')[1].split('_') if seg != '']
            _, _, _, hour, minute, second, _, day, month, year = segments
            year = int(year) + 2000
            file_timestamp = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)).strftime('%Y-%m-%dT%H%M%S')

            # find file location in `reorg` dir
            for file_name in FILE_NAMES:
                if file_name in str(annotation):
                    new_prefix = file_name
                    break
            if new_prefix is None:
                raise ValueError(f'Could not find file name prefix for {annotation}')

            new_name = f'{new_prefix}_{file_timestamp}.wav'
            new_names.append(new_name)
    # Toshiba files
    else:
        for file_name in FILE_NAMES:
            if file_name in str(annotation):
                new_prefix = file_name
                break
            if new_prefix is None:
                logging.warning(f'Could not find file name prefix (location) for {file_name}')
                new_prefix = 'unknown'
            new_name = f'{new_prefix}_{filename.name}'
            new_names.append(new_name)

    df['file'] = new_names

    return df[rename_cols.values()]
