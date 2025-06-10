import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

@dataclass
class PodcastEpisode:
    """Class for storing podcast episode information."""
    title: str
    description: str
    audio_url: str
    transcript_url: Optional[str] = None
    duration_ms: Optional[int] = None
    published_at: Optional[str] = None

class PodcastCollector:
    def __init__(self, 
                 spotify_client_id: str,
                 spotify_client_secret: str,
                 output_dir: str):
        """
        Initialize the podcast collector.
        
        Args:
            spotify_client_id: Spotify API client ID
            spotify_client_secret: Spotify API client secret
            output_dir: Directory to save collected data
        """
        self.sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=spotify_client_id,
                client_secret=spotify_client_secret
            )
        )
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # List of target podcasts
        self.target_podcasts = [
            "The Wild Project",
            "Aleja y La Grua",
            "No Hay Tos",
            "Bibliotequeando",
            "Advanced Spanish Podcast by Spanish Language Coach"
        ]
    
    def search_podcast(self, name: str) -> Optional[str]:
        """
        Search for a podcast on Spotify.
        
        Args:
            name: Podcast name to search for
            
        Returns:
            Spotify podcast ID if found, None otherwise
        """
        results = self.sp.search(q=name, type="show", limit=1)
        if results["shows"]["items"]:
            return results["shows"]["items"][0]["id"]
        return None
    
    def get_podcast_episodes(self, podcast_id: str, limit: int = 50) -> List[Dict]:
        """
        Get episodes for a podcast.
        
        Args:
            podcast_id: Spotify podcast ID
            limit: Maximum number of episodes to fetch
            
        Returns:
            List of episode information
        """
        episodes = []
        offset = 0
        
        while len(episodes) < limit:
            results = self.sp.show_episodes(
                podcast_id,
                limit=min(50, limit - len(episodes)),
                offset=offset
            )
            
            if not results["items"]:
                break
                
            episodes.extend(results["items"])
            offset += len(results["items"])
            
            if not results["next"]:
                break
        
        return episodes
    
    def download_audio(self, url: str, output_path: Path) -> bool:
        """
        Download audio file from URL.
        
        Args:
            url: Audio file URL
            output_path: Path to save the audio file
            
        Returns:
            True if download successful, False otherwise
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get("content-length", 0))
            
            with open(output_path, "wb") as f, tqdm(
                desc=output_path.name,
                total=total_size,
                unit="iB",
                unit_scale=True
            ) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    size = f.write(data)
                    pbar.update(size)
            
            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False
    
    def collect_podcasts(self):
        """
        Collect podcasts and their episodes.
        """
        for podcast_name in self.target_podcasts:
            print(f"\nProcessing podcast: {podcast_name}")
            
            # Search for podcast
            podcast_id = self.search_podcast(podcast_name)
            if not podcast_id:
                print(f"Podcast not found: {podcast_name}")
                continue
            
            # Create podcast directory
            podcast_dir = self.output_dir / podcast_name.replace(" ", "_")
            podcast_dir.mkdir(exist_ok=True)
            
            # Get episodes
            episodes = self.get_podcast_episodes(podcast_id)
            
            # Save episode metadata
            metadata = {
                "podcast_name": podcast_name,
                "spotify_id": podcast_id,
                "episodes": []
            }
            
            for episode in episodes:
                episode_info = {
                    "title": episode["name"],
                    "description": episode["description"],
                    "duration_ms": episode["duration_ms"],
                    "published_at": episode["release_date"],
                    "audio_url": episode["audio_preview_url"],
                    "transcript_url": None  # TODO: Implement transcript extraction
                }
                
                metadata["episodes"].append(episode_info)
                
                # Download audio
                if episode["audio_preview_url"]:
                    audio_path = podcast_dir / f"{episode['id']}.mp3"
                    self.download_audio(episode["audio_preview_url"], audio_path)
            
            # Save metadata
            with open(podcast_dir / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

def main():
    # TODO: Replace with actual Spotify API credentials
    spotify_client_id = "YOUR_CLIENT_ID"
    spotify_client_secret = "YOUR_CLIENT_SECRET"
    
    collector = PodcastCollector(
        spotify_client_id=spotify_client_id,
        spotify_client_secret=spotify_client_secret,
        output_dir="dataset_work/raw"
    )
    
    collector.collect_podcasts()

if __name__ == "__main__":
    main() 