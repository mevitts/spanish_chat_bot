"""
Audio processing module for recording and text-to-speech functionality.
"""

from .recorder import record_audio
from .tts import text_to_speech

__all__ = ['record_audio', 'text_to_speech'] 