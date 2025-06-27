from dotenv import load_dotenv
load_dotenv("tokens.env")


from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
import numpy as np
import traceback
import logging
from .audio import record_audio, text_to_speech
from .models import transcribe_audio, generate_response

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class AudioData(BaseModel):
    audioData: list[float]

class TextData(BaseModel):
    text: str

@app.post("/api/start-recording")
async def start_recording():
    try:
        audio = record_audio()
        return {"audioData": audio.tolist()}
    except Exception as e:
        logger.error(f"Error in start_recording: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
async def handle_transcription(audio: AudioData):
    try:
        audio_array = np.array(audio.audioData)
        # Get the recorded audio turn into an array and transcribe it
        text = transcribe_audio(audio=audio_array)
        return {"transcription": text}
    except Exception as e:
        logger.error(f"Error in handle_transcription: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def handle_generation(text_data: TextData): #since frontend sends in json form, need to introduce it as TextData to validate JSON
    try:
        logger.info(f"[testing] Starting generation for text: {text_data.text}")
        
        # Generate response and convert to speech
        # generate_response expects text and optional model_name and api_key
        logger.info("[testing] Calling generate_response...")
        response = generate_response(text=text_data.text)
        logger.info(f"[testing] Generated response: {response}")
        
        logger.info("[testing] Calling text_to_speech...")
        audio_url = text_to_speech(response)
        logger.info(f"[testing] Audio URL: {audio_url}")
        
        return {
            "response": response,
            "audioUrl": audio_url
        }
    except Exception as e:
        logger.error(f"Error in handle_generation: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Handle real-time updates if needed
