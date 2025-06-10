import os
import json
import torch
import librosa
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import Dataset, DatasetDict
import soundfile as sf
from tqdm import tqdm

@dataclass
class AudioSegment:
    """Class for storing audio segment information."""
    audio_path: str
    transcript: str
    start_time: float
    end_time: float
    speaker_id: str = None

class DatasetPreparator:
    def __init__(self, 
                 base_dir: str,
                 target_sr: int = 16000,
                 max_duration: float = 30.0):
        """
        Initialize the dataset preparator.
        
        Args:
            base_dir: Base directory for dataset
            target_sr: Target sampling rate (default: 16000 Hz)
            max_duration: Maximum duration for audio segments in seconds
        """
        self.base_dir = Path(base_dir)
        self.target_sr = target_sr
        self.max_duration = max_duration
        
        # Create necessary directories
        self.raw_dir = self.base_dir / "raw"
        self.processed_dir = self.base_dir / "processed"
        self.metadata_dir = self.base_dir / "metadata"
        
        for dir_path in [self.raw_dir, self.processed_dir, self.metadata_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def process_audio(self, audio_path: str) -> str:
        """
        Process audio file: normalize, resample, and save.
        
        Args:
            audio_path: Path to input audio file
            
        Returns:
            Path to processed audio file
        """
        # Load audio
        audio, sr = librosa.load(audio_path, sr=None)
        
        # Resample if necessary
        if sr != self.target_sr:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=self.target_sr)
        
        # Normalize audio
        audio = librosa.util.normalize(audio)
        
        # Save processed audio
        output_path = self.processed_dir / Path(audio_path).name
        sf.write(output_path, audio, self.target_sr)
        
        return str(output_path)
    
    def segment_audio(self, audio_path: str, transcript: str) -> List[AudioSegment]:
        """
        Segment audio into smaller chunks with corresponding transcripts.
        
        Args:
            audio_path: Path to audio file
            transcript: Full transcript text
            
        Returns:
            List of AudioSegment objects
        """
        # Load audio
        audio, sr = librosa.load(audio_path, sr=self.target_sr)
        
        # Simple segmentation based on silence
        intervals = librosa.effects.split(audio, top_db=20)
        
        segments = []
        for i, (start, end) in enumerate(intervals):
            duration = (end - start) / sr
            
            if duration > self.max_duration:
                # Split long segments
                num_splits = int(np.ceil(duration / self.max_duration))
                for j in range(num_splits):
                    split_start = start + j * int(self.max_duration * sr)
                    split_end = min(start + (j + 1) * int(self.max_duration * sr), end)
                    
                    segment_path = f"{Path(audio_path).stem}_segment_{i}_{j}.wav"
                    segment_path = self.processed_dir / segment_path
                    
                    sf.write(segment_path, audio[split_start:split_end], sr)
                    
                    segments.append(AudioSegment(
                        audio_path=str(segment_path),
                        transcript=transcript,  # TODO: Split transcript accordingly
                        start_time=split_start / sr,
                        end_time=split_end / sr
                    ))
            else:
                segment_path = f"{Path(audio_path).stem}_segment_{i}.wav"
                segment_path = self.processed_dir / segment_path
                
                sf.write(segment_path, audio[start:end], sr)
                
                segments.append(AudioSegment(
                    audio_path=str(segment_path),
                    transcript=transcript,  # TODO: Split transcript accordingly
                    start_time=start / sr,
                    end_time=end / sr
                ))
        
        return segments
    
    def create_dataset(self, segments: List[AudioSegment]) -> DatasetDict:
        """
        Create a HuggingFace dataset from processed segments.
        
        Args:
            segments: List of AudioSegment objects
            
        Returns:
            DatasetDict containing train/validation/test splits
        """
        # Convert segments to dataset format
        data = {
            "audio_path": [s.audio_path for s in segments],
            "transcript": [s.transcript for s in segments],
            "start_time": [s.start_time for s in segments],
            "end_time": [s.end_time for s in segments],
            "speaker_id": [s.speaker_id for s in segments]
        }
        
        # Create dataset
        dataset = Dataset.from_dict(data)
        
        # Split dataset
        dataset_dict = dataset.train_test_split(test_size=0.2)
        test_valid = dataset_dict["test"].train_test_split(test_size=0.5)
        
        return DatasetDict({
            "train": dataset_dict["train"],
            "validation": test_valid["train"],
            "test": test_valid["test"]
        })
    
    def save_dataset(self, dataset_dict: DatasetDict, name: str):
        """
        Save dataset to disk and optionally push to HuggingFace Hub.
        
        Args:
            dataset_dict: DatasetDict to save
            name: Name for the dataset
        """
        # Save locally
        dataset_dict.save_to_disk(self.base_dir / name)
        
        # Save metadata
        metadata = {
            "name": name,
            "description": "Spanish conversational audio dataset for fine-tuning Whisper",
            "language": "es",
            "license": "cc-by-nc-4.0",
            "size": {
                "train": len(dataset_dict["train"]),
                "validation": len(dataset_dict["validation"]),
                "test": len(dataset_dict["test"])
            }
        }
        
        with open(self.metadata_dir / f"{name}_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

def main():
    # Example usage
    preparator = DatasetPreparator("dataset_work")
    
    # TODO: Implement audio collection and transcript alignment
    # For now, this is a placeholder for the actual implementation
    
    print("Dataset preparation script ready. Implement audio collection and processing.")

if __name__ == "__main__":
    main() 