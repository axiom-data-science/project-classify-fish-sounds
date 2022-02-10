#!python
"""Names are mangled, so this script writes sample files using ISO datetimes as the name"""
from __future__ import annotations
import datetime
import logging
import shutil
from pathlib import Path

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')


def get_file_timestamp(fname: Path) -> datetime.datetime | None:
    """Given path to old file name, return the timestap as a datetime"""
    # Old style names
    # 0059.DSG_RAWD_HMS__7__0__0__DMY_27__1_16.wav
    # rileys-hump 2009 names
    # 3035.DSG_HMS_12_50_ 0__DMY_ 4_ 7_ 9.wav
    # steamboat
    # DSG_6_RG_3-000.5078.YMD_2009_04_27_HMS_21_30_00.dsg_RAWD_HMS_21_30__0__DMY_27__4__9.wav
    try:
        if 'rileys-hump' in str(fname) and '2009' in str(fname):
            logging.info(f'rileys-hump 2009 file: {fname}')
            # pull out empty ('') segments, exist because of different number of '_' in filename
            segments = [seg for seg in fname.name.split('.')[1].split('_') if seg != '']
            _, _, hour, minute, second, _, day, month, year = segments
        elif 'steamboat' in str(fname):
            logging.info(f'steamboat file: {fname}')
            segments = [seg for seg in fname.name.split('.')[2].split('_') if seg != '']
            # YMD_2009_04_27_HMS_21_30_00
            _, year, month, day, _, hour, minute, second = segments
        else:
            # pull out empty ('') segments, exist because of different number of '_' in filename
            segments = [seg for seg in fname.name.split('.')[1].split('_') if seg != '']
            _, _, _, hour, minute, second, _, day, month, year = segments
    except ValueError:
        logging.warn(f'Unable to split {fname}, skipping')
        return None

    try:
        if not 'steamboat' in str(fname):
            dt = datetime.datetime(int(year) + 2000, int(month), int(day), int(hour), int(minute), int(second))
        else:
            dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    except:
        logging.warn(f'Unable to parse {fname}, skipping')
        dt = None

    return dt



def copy_files(sample_dir: Path, output_dir: Path, output_name_prefix: str) -> None:
    """Given directory with sample files, *COPY* files to new standard to ease data munging.

    Notes
    -----
    - Copying the files here to ensure that the new files match the originals.  Old files will be manually deleted.
    - Files saved in yyyy/mm/dd/<name>_yyyy-mm-dd_HH-MM-SS.wav
    """
    original_files = list(sample_dir.glob('**/*.wav'))
    if len(original_files) == 0:
        original_files = list(sample_dir.glob('**/*.WAV'))

    for file in original_files:
        timestamp = get_file_timestamp(file)

        try:
            # Probably Toshiba files
            if timestamp is None:
                outdir = output_dir / output_name_prefix
                outdir.mkdir(exist_ok=True, parents=True)
                new_file = outdir / file.name
            else:
                outdir = output_dir / str(timestamp.year) / f'{timestamp.month:02}' / f'{timestamp.day:02}'
                outdir.mkdir(exist_ok=True, parents=True)
                new_file = outdir / f'{output_name_prefix}_{timestamp.strftime("%Y-%m-%dT%H-%M-%S")}.wav'
            logging.info(f'Copying {file} to {new_file}')
            shutil.copy2(file, new_file)
        except:
            logging.warning(f'Unable to copy {file}')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'sample_dir',
        type=Path,
        help='Path to sample files'
    )
    parser.add_argument(
        'output_dir',
        type=Path,
        help='Path to output dir'
    )
    parser.add_argument(
        'output_name_prefix',
        type=str,
        help='Name of output files (e.g. <name>_yyyy-mm-dd_HH-MM-SS.wav)'
    )

    args = parser.parse_args()
    args.output_dir.mkdir(exist_ok=True, parents=True)
    copy_files(args.sample_dir, args.output_dir, args.output_name_prefix)


if __name__ == '__main__':
    main()
