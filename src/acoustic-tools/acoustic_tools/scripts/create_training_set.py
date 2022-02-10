#!python
"""Create training dateset given sample files and annotation DataFrame."""
from __future__ import annotations
import datetime
import itertools
import logging
import shutil
from pathlib import Path

import pandas as pd

from acoustic_tools import sample

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')



def create_training_set(sample_dir: Path, annotations_path: Path, outdir: Path, length: float | None, lpf: float | None, signal_level: int | None) -> None:
    """Given an annotation DataFrame, copy annotated files into new directory for model dev.

    Parameters
    ----------
    sample_dir: Path
        Path to directory with sample files
    annotations: Path
        Path to annotations file.
    outdir: Path
        Path to directory to write sampled data.  Whole files will be copied to f'{outdir}-whole'.
    length: float
        Length of samples to create
    lpf: float
        Frequency at which to low pass filter
    signal_level: int
        If provided, only calls of the given signal level will be used (1: high SNR, 2: medium SNR, 3: low SNR)

    Notes
    -----
    Files are copied into a directory structure to facilitate model development:
    outdir:
    |_ call-variant-1
    | |_ clean
    | |_ call-cutoff
    | |_ call-overlap
    | |_ call-cutoff-and-overlap
    |_ call-variant-2
    |
    ...
    """
    logging.info(f'Creating sample from {annotations_path}')
    annotations = pd.read_csv(annotations_path)
    # Ensure call_variant is an int
    annotations = annotations.astype({'call_variant': int}, errors='raise')

    outdir.mkdir(exist_ok=True)
    whole_outdir = Path(f'{outdir}-whole')
    whole_outdir.mkdir(exist_ok=True)

    CALL_VARIANTS = [
        1,  # grouper 1
        2,  # grouper 2
        3,  # grouper grunt
        4,  # grouper spawning rush
        5,  # grouper chorus < 50% of file
        6,  # grouper chrous > 50% of file
        8,  # unidentified sound type
        9,  # red grouper 1
        10,  # red grouper 2
        17,  # red hind 1
        18,  # red hind 2
        19,  # red hind 3
        25,  # goliath grouper 1
        27,  # multi-phase goliath grouper
        28,  # sea trout chorus
        29,  # silver perch call
        30,  # snowy grouper primary call
        33,  # gag grouper primary call
        34,  # manatee primary call
        35,  # mantaee click
        36,  # mantee chrip
    ]
    EMPTY_CALLS = [
        7,  # no calls
        15,  # no red grouper sound
        23,  # no red hind
        26,  # no goliath grouper calls
    ]
    CALL_OVERLAP = [True, False]
    CALL_CUTOFF = [True, False]
    for params in itertools.product(CALL_VARIANTS, CALL_OVERLAP, CALL_CUTOFF):
        call_variant = params[0]
        call_overlap = params[1]
        call_cutoff = params[2]
        signal_level = params[3]

        logging.info(f'Sampling {call_variant}:, call overlap: {call_overlap}, call cutoff: {call_cutoff}')
        # If the call is cutoff and overlapping
        if call_overlap and call_cutoff:
            variant_outdir = outdir / f'call-{call_variant}' / 'call-cutoff-and-overlap'
            variant_whole_outdir = whole_outdir / f'call-{call_variant}' / 'call-cutoff-and-overlap'
        # Calls are only overlapping
        elif call_overlap:
            variant_outdir = outdir / f'call-{call_variant}' / 'call-overlap'
            variant_whole_outdir = whole_outdir / f'call-{call_variant}' / 'call-overlap'
        # Calls are only cut-off
        elif call_cutoff:
            variant_outdir = outdir / f'call-{call_variant}' / 'call-cutoff'
            variant_whole_outdir = whole_outdir / f'call-{call_variant}' / 'call-cutoff'
        # Otherwise, there's no overlapping and it's not cutoff -> "clean"
        else:
            variant_outdir = outdir / f'call-{call_variant}' / 'clean'
            variant_whole_outdir = whole_outdir / f'call-{call_variant}' / 'clean'
        variant_outdir.mkdir(exist_ok=True, parents=True)
        variant_whole_outdir.mkdir(exist_ok=True, parents=True)

        samples = annotations.query(
            f'call_variant=={call_variant} and '
            f'call_overlap=={call_overlap} and '
            f'call_cutoff=={call_cutoff}'
        )
        if signal_level is not None:
            logging.info(f'Including only samples of level: {signal_level}')
            samples = samples.query(f'signal_level=={signal_level}')

        for ix, row in samples.iterrows():
            try:
                fname = row.file
            except KeyError:
                logging.warning(f'Sample fname {row.file} not available')
                continue
            name, datestr = fname.split('.')[0].split('_')
            filedate = datetime.datetime.strptime(datestr, '%Y-%m-%dT%H%M%S')
            fname = f'{name}_{filedate:%Y-%m-%dT%H-%M-%S}.wav'
            # <sample-dir>/<name>/yyyy/mm/dd/<name>_yyyy-mm-ddTHHMMSS.wav
            if name == 'exxon':
                sample_dir = 'exxon-template-tower'

            infile = Path(f'{sample_dir}/{name}/{filedate.year}/{filedate.month:02}/{filedate.day:02}/{fname}')
            outfile = variant_outdir / f'sample-{ix:04}'
            whole_outfile = variant_whole_outdir / f'sample-{ix:04}'
            end_time = row.start_time + row.call_length

            logging.info(f'Creating sample {outfile}')
            try:
                sample.create_sample(infile, outfile, row.start_time, end_time, length, lpf)
            except:
                logging.warning(f'Problem creating samples from {infile}')
            try:
                shutil.copy(infile, whole_outfile)
            except:
                logging.warning(f'Problem copying whole sample {infile}')

    for empty_call in EMPTY_CALLS:
        logging.info(f'Sampling empty call {empty_call}')
        # All empty calls go into a single dir for training
        call_outdir = outdir / 'call-0'
        call_outdir.mkdir(exist_ok=True, parents=True)
        call_whole_outdir = whole_outdir / 'call-0'
        call_whole_outdir.mkdir(exist_ok=True, parents=True)

        samples = annotations.query(
            f'call_variant=={empty_call}'
        )
        for ix, row in samples.iterrows():
            try:
                fname = row.file
            except KeyError:
                logging.warning(f'Sample fname {row.file} not available')
                continue
            name, datestr = fname.split('.')[0].split('_')
            filedate = datetime.datetime.strptime(datestr, '%Y-%m-%dT%H%M%S')
            fname = f'{name}_{filedate:%Y-%m-%dT%H-%M-%S}.wav'
            # <sample-dir>/<name>/yyyy/mm/dd/<name>_yyyy-mm-ddTHHMMSS.wav
            infile = Path(f'{sample_dir}/{name}/{filedate.year}/{filedate.month:02}/{filedate.day:02}/{fname}')
            outfile = call_outdir / f'sample-{ix:04}'
            whole_outfile = call_whole_outdir / f'sample-{ix:04}'
            end_time = row.start_time + row.call_length

            logging.info(f'Creating sample {outfile} from {infile}')

            try:
                sample.create_sample(infile, outfile, row.start_time, end_time, length, lpf)
            except:
                logging.warning(f'Problem creating samples from {infile}')
            try:
                shutil.copy(infile, whole_outfile)
            except:
                logging.warning(f'Problem copying whole sample {infile}')

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'sample_dir',
        type=Path,
        help='Path to directory with samples'
    )
    parser.add_argument(
        'annotations',
        type=Path,
        help='Path to annotation csv file.'
    )
    parser.add_argument(
        'output_dir',
        type=Path,
        help='Path to output directory'
    )
    parser.add_argument(
        '--length',
        type=float,
        help='Length of sample',
        default=None
    )
    parser.add_argument(
        '--lpf',
        type=float,
        help='Hz to low pass filter',
        default=None
    )
    parser.add_argument(
        '--snr_level',
        type=int,
        help='SNR level to optionally filter for.  (1: High, 2: Medium, 3: Low)',
        default=None
    )

    args = parser.parse_args()
    logging.info(f'Reading annotations from {args.annotations}')
    logging.info(f'Creating samples in {args.output_dir} from files in {args.sample_dir}')

    create_training_set(args.sample_dir, args.annotations, args.output_dir, args.length, args.lpf, args.snr_level)


if __name__ == '__main__':
    main()
