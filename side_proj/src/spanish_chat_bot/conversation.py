"""
Main conversation handler that orchestrates the Spanish chat bot.
"""
from typing import Optional
import time
from .audio import record_audio, text_to_speech
from .models import transcribe_audio, generate_response

class Conversation:
    def __init__(self):
        """Initialize the conversation handler."""
        self.is_active = False
        self.conversation_history = []

    def start(self):
        """Start the conversation loop."""
        self.is_active = True
        print("¡Hola! Estoy listo para conversar. Presiona Ctrl+C para salir.")
        
        while self.is_active:
            try:
                #record audio
                print("\nEscuchando...")
                audio = record_audio()
                
                #transcribe audio to text
                text = transcribe_audio(audio)
                if not text:
                    print("No pude entender eso. ¿Podrías repetirlo?")
                    continue
            
                
                #generate response
                response = generate_response(text)
                
                #Convert response to speech and play it
                text_to_speech(response)
                
                #conversation history
                self.conversation_history.append({
                    'user': text,
                    'bot': response,
                    'timestamp': time.time()
                })
                
            except KeyboardInterrupt:
                print("\n¡Hasta luego!")
                self.is_active = False
            except Exception as e:
                print(f"Lo siento, hubo un error: {str(e)}")
                continue
            
    def stop(self):
        """Stop the conversation."""
        self.is_active = False


def main():
    """Main entry point for the conversation."""
    conversation = Conversation()
    conversation.start()


if __name__ == "__main__":
    main()