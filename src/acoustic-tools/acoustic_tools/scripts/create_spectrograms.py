#!python
"""Create spectrograms from audio files using matplotlib"""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Union

import click
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)


@dataclass
class FFTConfig():
    n_fft: Union[int, None] = 2**12
    win_length: Union[int, None] = None
    hop_length: int = 512
    sr: int = 22_050
    db: bool = False
    mel: bool = False
    fmin: int = 50
    fmax: int = 10_000
    y_axis: str = 'linear'
    denoise: Union[str, None] = None
    pcen: bool = False
    cmap: str = 'magma'
    n_mels: int = 128
    vmin: Union[float, None] = None
    vmax: Union[float, None] = None
    bandpass: bool = True
    ylim: Union[Tuple[float, float], None] = (0, 512)

def load_wav(fpath):
    y, sr = librosa.load(fpath)
    audio, _ = librosa.effects.trim(y)

    return audio, sr


def calc_stft(audio, fft_config):
    stft = librosa.stft(audio, n_fft=fft_config.n_fft, hop_length=fft_config.hop_length, win_length=fft_config.win_length)
    return np.abs(stft)


def plot_spec(fpath: Path, output: Path, fft_config: FFTConfig):
    audio, sr = load_wav(fpath)
    if fft_config.bandpass:
        audio = fish_filter(audio, fs=sr)

    stft = calc_stft(audio, fft_config)

    if fft_config.pcen:
        # Scale PCEN: https://librosa.org/doc/latest/generated/librosa.pcen.html?highlight=pcen#librosa.pcen
        stft = librosa.pcen(stft * (2**31), sr=fft_config.sr, hop_length=fft_config.hop_length)
        fft_config.db = True

    if fft_config.mel:
        stft = librosa.feature.melspectrogram(
            y=audio,
            sr=fft_config.sr,
            n_mels=fft_config.n_mels,
            fmin=fft_config.fmin,
            fmax=fft_config.fmax
        )
        # Mel is in db
        fft_config.db = True

    if fft_config.db:
        stft = librosa.amplitude_to_db(stft, ref=np.max)

    fig, ax = plt.subplots(1, 1)
    _ = librosa.display.specshow(
        stft,
        sr=fft_config.sr,
        hop_length=fft_config.hop_length,
        x_axis='time',
        y_axis=fft_config.y_axis,
        fmin=fft_config.fmin,
        fmax=fft_config.fmax,
        cmap=fft_config.cmap,
        ax=ax,
        vmin=fft_config.vmin,
        vmax=fft_config.vmax
    )
    ax.set_axis_off()
    if fft_config.ylim is not None:
        ax.set_ylim(fft_config.ylim)

    if output:
        fig.savefig(output, bbox_inches='tight', pad_inches=0)
        plt.close(fig=fig)

    plt.close('all')


def fish_filter(call, low=50, high=512, order=8, fs=22_050):
    sos = signal.butter(order, [low, high], 'bandpass', output='sos', fs=fs)
    return signal.sosfilt(sos, call)


@click.command()
@click.argument('path_to_wavs', type=click.Path(exists=True))
@click.argument('path_to_output', type=click.Path())
def main(path_to_wavs: Path, path_to_output: Path) -> None:
    """Given paths to input audio files save spectrograms in output directory"""
    logging.info(f'Saving spectrograms from audio files in {path_to_wavs} in {path_to_output}')
    base_out = Path(path_to_output)
    path_to_wavs = Path(path_to_wavs)

    fft_config = FFTConfig()

    for training_file in path_to_wavs.glob('**/*.wav'):
        logging.info(f'Converting {training_file}')
        output_dir = base_out / str(training_file.parents[0])
        output_dir.mkdir(exist_ok=True, parents=True)
        output_name = str(training_file.name).replace('.wav', '.png')
        output_file = output_dir / output_name
        try:
            plot_spec(training_file, output_file, fft_config)
        except:
            logging.error(f'Failed to convert {training_file}')


if __name__ == '__main__':
    main()
