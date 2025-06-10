# Spanish Podcast Dataset Preparation

This directory contains scripts and tools for preparing a Spanish podcast dataset for fine-tuning the Whisper model.

## Overview

The dataset preparation process consists of the following steps:

1. **Audio Collection**: Download audio from Spanish podcasts using the Spotify API
2. **Audio Processing**: Normalize, resample, and segment audio files
3. **Transcript Alignment**: Align transcripts with audio segments
4. **Dataset Creation**: Create a HuggingFace dataset for fine-tuning

## Directory Structure

```
dataset_work/
├── raw/                    # Raw audio files and metadata
├── processed/              # Processed audio segments
├── metadata/              # Dataset metadata and statistics
├── requirements.txt       # Python dependencies
├── dataset_preparation.py # Core dataset preparation script
├── podcast_collector.py   # Podcast audio collection script
└── README.md             # This file
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Spotify API credentials:
   - Create a Spotify Developer account
   - Create a new application to get client ID and secret
   - Update the credentials in `podcast_collector.py`

## Usage

1. Collect podcast audio:
```bash
python podcast_collector.py
```

2. Process audio and create dataset:
```bash
python dataset_preparation.py
```

## Dataset Format

The final dataset will be in HuggingFace's dataset format with the following structure:

- **audio_path**: Path to audio segment file
- **transcript**: Corresponding transcript text
- **start_time**: Start time in seconds
- **end_time**: End time in seconds
- **speaker_id**: Speaker identifier (if available)

## Notes

- Audio files are processed to 16kHz mono WAV format
- Segments are limited to 30 seconds maximum
- Dataset is split into train/validation/test sets (80/10/10)
- Metadata includes dataset statistics and processing information

## TODO

- [ ] Implement transcript extraction from podcast sources
- [ ] Add speaker diarization support
- [ ] Implement quality checks for audio and transcripts
- [ ] Add data augmentation options
- [ ] Create visualization tools for dataset statistics 