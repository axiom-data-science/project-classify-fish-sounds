"""Functions for processing wav files."""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pydub


def create_sample(
    fpath_in: Path,
    fpath_out: Path,
    time_start: float,
    time_end: float,
    length: float | None = None,
    pad: float=0,
    lpf: float | None = None
    ) -> None:
    """Given input and output paths, sample time start and time end, add a pad and save to a new file."""
    sample = pydub.AudioSegment.from_wav(fpath_in)
    if lpf:
        sample = sample.low_pass_filter(lpf)

    if not pad:
        pad = 0

    # convert s to ms and add padding
    start_time = int(max(0, (time_start - pad) * 1000))
    last_time = len(sample)
    end_time = int(min(last_time, (time_end + pad) * 1000))
    clip = sample[start_time:end_time]

    # Create sub samples of length `length`
    if length:
        clip_length = len(clip)
        length = int(length * 1000)
        for subclip_ix, start_ix in enumerate(np.arange(0, clip_length, length)):
            end_ix = min(last_time, start_ix + length)
            subclip = clip[start_ix:end_ix]
            # some samples are length 0, skip them
            if len(subclip) == 0:
                continue
            subclip_name = fpath_out.name + f"-{subclip_ix:04}.wav"
            subclip.export(fpath_out.parent / subclip_name, format='wav')
    else:
        clip_name = fpath_out.name + ".wav"
        clip.export(fpath_out.parent / clip_name, format='wav')
