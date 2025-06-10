''' 
Converts text response to audio
'''
import sounddevice as sd
from scipy.io import wavfile
from TTS.api import TTS


def text_to_speech(text, output_path="output.wav"):
    """
    Take text input and convert it to wav file
    
    Args:
        text (string): Generated text from response generator
        output_path (string): path for wav file output
    Returns:
        string: path to wav file of response
    """
    
    try: 
    # Initialize TTS with Spanish xtts model
        tts = TTS(model_name="tts_models/es/css10/vits", progress_bar=False)
        
        # Generate speech
        tts.tts_to_file(text=text, file_path=output_path)
        
        # Play the audio
        sample_rate, audio = wavfile.read(output_path)
        sd.play(audio, sample_rate)
        sd.wait()
        
        return output_path
    
    except Exception as e:
        raise RuntimeError(f"Failed to convert text to audio: {str(e)}")
        