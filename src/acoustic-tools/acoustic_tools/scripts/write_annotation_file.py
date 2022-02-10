#!python
"""Write csv file with Black Grouper annotations from a direcotry combined and cleaned."""
import logging
from pathlib import Path

import pandas as pd

from acoustic_tools import annotation

logging.basicConfig(format='%(process)s - %(levelname)s: %(message)s', level=logging.INFO)


def read_annotation_files(annotation_dir: Path, glob_str: str) -> pd.DataFrame:
    """Given dir with annotation files and glob string for files, return all annotations as DataFrame"""
    annotation_files = list(annotation_dir.glob(glob_str))
    annotation_files.sort()

    dfs = []
    for annotation_file in annotation_files:
        logging.info(f'Reading annotation file {annotation_file}')
        try:
            df = annotation.read_annotation_file(annotation_file)
        except Exception as e:
            logging.warning(f'Failed to read annotation file {annotation_file}')
            continue
        dfs.append(annotation.read_annotation_file(annotation_file))

    return pd.concat(dfs)


def write_annotation_file(annotation_dir: Path, glob_str: str, output_file: Path) -> None:
    """Given a directory with annotation files and a glob string, write combined annotations to the given output file."""
    logging.info(f'Reading annotation files from {annotation_dir} using {glob_str} glob string')

    annotation_df = read_annotation_files(
        annotation_dir,
        glob_str,
    )

    logging.info(f'Writing combined annotation data to {output_file}')
    annotation_df.to_csv(output_file, index=False)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'annotation_dir',
        type=Path,
        help='Path to directory with annotation text files'
    )
    parser.add_argument(
        'output_file',
        type=Path,
        help='Path to output file name'
    )
    parser.add_argument(
        '--glob_str',
        type=str,
        default='*.txt',
        help='String to glob appropriate annotation files to combine'
    )
    args = parser.parse_args()
    output_dir = args.output_file.parent
    output_dir.mkdir(exist_ok=True)

    write_annotation_file(
        args.annotation_dir,
        args.glob_str,
        args.output_file
    )


if __name__ == '__main__':
    main()
