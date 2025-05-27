# Spanish Conversational Voice Bot (Whisper + LLM + TTS)

This project is a modular, voice-based Spanish conversational bot that enables **spoken conversations** in Spanish. It uses **Whisper** for speech-to-text, a Spanish-capable **language model** for generating responses, and **text-to-speech** synthesis to reply vocally.

**Status: Active Development**

 The Whisper model is currently being **fine-tuned** with a dataset of Spanish audio. Other modules (response generation and TTS) are still being developed.

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

