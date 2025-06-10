"""
Audio transcription functionality using Whisper model.
"""

import torch
from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
    WhisperFeatureExtractor,
    WhisperTokenizer
)
from typing import Optional, Union
import numpy as np


class Transcriber:
    def __init__(self, model_name: str = "openai/whisper-small", device: Optional[str] = None):
        """
        Initialize the transcriber with Whisper model.
        
        Args:
            model_name (str): Name of the Whisper model to use
            device (str, optional): Device to run the model on ('cuda' or 'cpu')
        """
        # looks for cuda device to run model on
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
        self.device = device
        self.feature_extractor = WhisperFeatureExtractor.from_pretrained(model_name)
        self.tokenizer = WhisperTokenizer.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name).to(self.device)
        
        # Configure model for Spanish + transcription
        self.model.config.forced_decoder_ids = self.tokenizer.get_decoder_prompt_ids(
            language="spanish",
            task="transcribe"
        )

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        """
        Transcribe audio to text.
        
        Args:
            audio (numpy.ndarray): Audio array
            sample_rate (int): Audio sample rate
            
        Returns:
            str: Transcribed text
        """
        #process audio to tensors
        inputs = self.feature_extractor(
            audio,
            sampling_rate=sample_rate,
            return_tensors="pt"
        )
        input_features = inputs.input_features.to(self.device)
        
        # Generate transcription
        predicted_ids = self.model.generate(
            input_features,
            max_length=448,
            num_beams=5, 
            temperature=0.7
        )
        transcription = self.tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        return transcription


# Create a singleton instance, more than one transcriber != good
_transcriber: Optional[Transcriber] = None

def transcribe_audio(audio: np.ndarray, sample_rate: int = 16000, model_name: str = "openai/whisper-small") -> str:
    """
    Global function to transcribe audio using the singleton transcriber.
    
    Args:
        audio (numpy.ndarray): Audio array
        sample_rate (int): Audio sample rate
        model_name (str): Name of the Whisper model to use
        
    Returns:
        str: Transcribed text
    """
    global _transcriber
    if _transcriber is None:
        _transcriber = Transcriber(model_name=model_name)
    return _transcriber.transcribe(audio, sample_rate) 