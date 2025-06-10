# Spanish Chat Bot

A conversational AI system for Spanish language interaction, featuring speech-to-text, text generation, and text-to-speech capabilities.

## Features

- Audio recording with noise filtering
- Speech-to-text using Whisper model
- Response generation using Gemini model
- Text-to-speech using TTS library
- Continuous conversation loop

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.config` file with your API keys:
```
GOOGLE_API_KEY=your_google_api_key
HF_TOKEN=your_huggingface_token
```

## Usage

Run the conversation:
```python
from spanish_chat_bot import Conversation

# Create and start a conversation
conversation = Conversation()
conversation.start()
```

Or run it directly as a module:
```bash
python -m spanish_chat_bot
```

## Project Structure

```
spanish_chat_bot/
|── notebooks/
|           ├──inference_pipeline.ipynb
│           └──model_finetune.ipynb
├── src/
│   └── spanish_chat_bot/
│       ├── audio/
│       │   ├── __init__.py
│       │   ├── recorder.py
│       │   └── tts.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── transcriber.py
│       │   └── response_generator.py
│       ├── __init__.py
│       └── conversation.py
├── requirements.txt
└── README.md
```

## Dependencies

- PyTorch
- Transformers
- SoundDevice
- NumPy
- SciPy
- Python-dotenv
- Google Generative AI
- TTS
- Datasets
- Evaluate
- Weights & Biases

## License

MIT License 