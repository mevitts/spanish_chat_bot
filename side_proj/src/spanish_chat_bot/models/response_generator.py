'''
Generate text response
'''
from dotenv import load_dotenv
load_dotenv("tokens.env")
import os
from typing import Optional, List
import google.generativeai as gem
from google.api_core import exceptions as google_exceptions

class ResponseGenerator:
    def __init__(self, model_name: str = "gemini-2.0-flash", api_key: Optional[str] = None):
        '''
        Initialize generator with model.
        
        Args:
            model_name (string): name of generative model to use
            api_key (str, optional): API key for model use if necessary. If not provided, will look for in env
        '''
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found. Please provide it or set GEMINI_API_KEY environment variable.")
            
        # Configure the API
        gem.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = gem.GenerativeModel(model_name)
        
        # Optional: Store conversation history
        self.conversation_history: List[dict] = []

    def generate(self, text: str) -> str:
        """
        Generate a response to the user's speech
        
        Args:
            text (str): user's speech input converted to text
        Returns:
            str: Generated text
        Raises:
            RuntimeError: If there's an error generating the response
        """
        try:
            response = self.model.generate_content(
                    f"Eres un asistente conversacional en español. Adaptarse al contexto de la conversación. "
                    f"(Por ejemplo: si la persona te diga algo como si fuera tu amigo o un familiar, respondele con ese rol.)"
                    f"Tu no eres un chatbot, eres la persona."
                    f"Mantenga la duración de tu respuesta corta. Responde de manera natural y conversacional a: {text}"
                )
            
            if not response or not response.text:
                raise RuntimeError("Received empty response from model")
                
            return response.text
            
        except google_exceptions.ResourceExhausted:
            raise RuntimeError("API rate limit exceeded. Please try again later.")
        except google_exceptions.ServiceUnavailable:
            raise RuntimeError("Gemini API service is currently unavailable. Please try again later.")
        except google_exceptions.InvalidArgument as e:
            raise RuntimeError(f"Invalid input to model: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {str(e)}")


# Create a singleton instance
_generator: Optional[ResponseGenerator] = None

def generate_response(text: str, model_name: str = "gemini-2.0-flash", api_key: Optional[str] = None) -> str:
    """
    Global function to generate responses using the singleton generator.
    
    Args:
        text (str): Text to generate response for
        model_name (str): Name of the model to use
        api_key (str, optional): API key for the model
        
    Returns:
        str: Generated response
    """
    global _generator
    if _generator is None:
        _generator = ResponseGenerator(model_name=model_name, api_key=api_key)
    return _generator.generate(text)