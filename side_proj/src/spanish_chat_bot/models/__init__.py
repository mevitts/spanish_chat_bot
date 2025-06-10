"""
Model-related functionality for transcription and response generation.
"""

from .transcriber import transcribe_audio
from .response_generator import generate_response

__all__ = ['transcribe_audio', 'generate_response'] 