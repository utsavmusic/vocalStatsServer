import librosa
import numpy as np

def get_frequency_data(y, sr):
    stft = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)
    avg_freq = np.mean(stft, axis=1)
    return list(zip(freqs.tolist(), avg_freq.tolist()))