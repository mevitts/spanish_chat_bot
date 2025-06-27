# Spanish Conversational Voice Bot (Whisper + LLM + TTS)

This project is a modular, voice-based Spanish conversational bot that enables **spoken conversations** in Spanish. It uses **Whisper** for speech-to-text, a Spanish-capable **language model** for generating responses, and **text-to-speech** synthesis to reply vocally.

**Status: Proof of Concept Operational**

The project is currently a fully functional minimal viable product, with its core voice-to-voice pipeline being operational. In this pipeline, the user will press the record button and speak in Spanish, which will then be transcibed by Whsper and passed to generate a response from a language model that will be played back to the user as audio. It currently runs locally and has a basic frontend for user interaction and conversation history. 

Expansion on this proof of concept is actively in development. 

## Inspiration

This project provides accessible language learning via natural human-computer interaction. Participation in conversations in the target language is one of the best ways to advance language learning. As a result, this project provides a valuable opportunity for those who do not have the ability to have conversations in Spanish with other speakers.

Also, as a recent graduate, this project helps me sharpen my skills in:
- Fine-tuning foundational models for practical tasks
- Gain further experience with Whisper, LLMs, TTS and HuggingFace pipelines
  
## Project Goals

- Transcribe Spanish audio to text using a fine-tuned Whisper model
- Generate conversational, Spanish responses using a text generation model
- Convert response text back to natural sounding Spanish speech
- Support various Spanish accents
- Enable full voice-to-voice interaction pipeline

## Pipeline Overview

```bash
[Mic/Audio File]
      ↓
[Speech-to-Text]
      ↓
[Natural Language Response]
      ↓
[Text-to-Speech]
      ↓
[Voice Output]
```

## Future Goals/Roadmap

The future of this project is expanding on the basic proof of concept to a more robust and user friendly application. Key additions include:

- **Deployment:** Package the application and deploy it to a cloud platform to make it accessible beyond a local machine.
- **Conversation Memory:** Implement a memory module that allows the bot to recall more of the conversation than the current input, creating a more immersive and coherent conversation.
- **UX/UI Enhancements:** Move on from a proof of concept user interface to have it be more intuitive, and user friendly, adopting its own design to better match its function.
- **Greater Model Fine-Tuning:** The first attempt at fine-tuning the Whisper model resulted in worse transcription than the base model, leading to current transcription tasks being assigned to the base model. As a result, being able successfully fine-tune the model on a wide variety of Spanish dialects and accents would be a key step in increasing transcription accuracy. This is a very important aspect as many of the users would still be learning Spanish, so their speaking abilities will lack a natural flow and accent that the base Whisper model would be accustomed to. 


