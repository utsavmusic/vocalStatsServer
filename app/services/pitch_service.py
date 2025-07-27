import librosa
import numpy as np
import os

def get_extreme_notes(y, sr):
    import re

    n_fft = 2048
    hop_length = 512
    stft = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

    valid_notes = []

    for frame in stft.T:
        frame_energy = np.max(frame)
        if frame_energy < 0.01:  # Skip silent or quiet frames
            continue

        peak_bin = np.argmax(frame[:n_fft // 2])
        peak_freq = freqs[peak_bin]
        
        if np.isinf(peak_freq) or peak_freq <= 0:
            continue  # Skip this frame

        note = librosa.hz_to_note(peak_freq)

        # Parse octave correctly
        match = re.match(r'^([A-G]#?)(\d+)$', note)
        if not match:
            continue

        octave = int(match.group(2))
        if 3 <= octave <= 5:
            valid_notes.append((peak_freq, note))

    if not valid_notes:
        return {
            "min_note": None,
            "max_note": None,
            "min_freq_hz": None,
            "max_freq_hz": None
        }

    min_freq, min_note = min(valid_notes, key=lambda x: x[0])
    max_freq, max_note = max(valid_notes, key=lambda x: x[0])

    return {
        "min_freq_hz": min_freq,
        "max_freq_hz": max_freq,
        "min_note": min_note,
        "max_note": max_note,
    }


