#!python
from pathlib import Path

import pandas as pd


BAD_FILES = '/Users/jesse/Downloads/acoustic-data-annotations/diff-selection-files/bad-files.txt'

def main(bad_files=BAD_FILES):
    bad_files = pd.read_csv(bad_files)

    for row in bad_files.iterrows():
        input_file = row[1][0]
        print(input_file)

        df = pd.read_csv(input_file, sep='\t')
        df.to_csv(input_file, index=False)


if __name__ == '__main__':
    main()
