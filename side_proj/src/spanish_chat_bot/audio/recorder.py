"""
Audio recorder.
"""
import sounddevice as sd
import numpy as np
from scipy.signal import butter, filtfilt


def record_audio(duration=5, sample_rate=16000, cutoff_freq=100, filter_order=4):
    """
    Record audio for set duration and process it
    
    Args:
        duration (int): Amount of time recording user audio in seconds
        sample rate (int): sample rate to record audio in Hz
        cutoff_freq (int): Cutoff frequency for high-pass filter in Hz
        filter_order (int): Order of the Butterworth filter
    Returns:
        numpy.ndarray: Processed audio signal normalized to [-1, 1]
        
    """
    try:
        myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        
        #convert to single array, then normalize audio
        audio = myrecording.flatten()
        audio = audio / np.max(np.abs(audio))
        
        # apply filter to reduce noise
        nyquist = sample_rate / 2 #nyquist rate is 1/2 of the frequency
        
        #filter_order: higher order = sharper cutoff
        #cutoff_freq/nyquist normalizes the cutoff frequency
        #btype = high pass filter
        b, a = butter(filter_order, cutoff_freq/nyquist, btype='high')
        audio = filtfilt(b, a, audio)
        
        #normalize again
        audio = audio / np.max(np.abs(audio))
        return audio
        
    except Exception as e:
        raise RuntimeError(f"Failed to record audio: {str(e)}")