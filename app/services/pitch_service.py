import librosa
import numpy as np
import os

def get_high_low_notes(y, sr):
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[magnitudes > np.median(magnitudes)]

    if len(pitch_values) == 0:
        return None, None

    low_freq = np.min(pitch_values)
    high_freq = np.max(pitch_values)

    return librosa.hz_to_note(low_freq), librosa.hz_to_note(high_freq)