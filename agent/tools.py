from youtube_search import YoutubeSearch
import json
from langchain_community.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

@tool
def search_youtube(query: str):
    """
    Searches YouTube for the top 10 videos based on a query.

    Args:
        query: The search query.

    Returns:
        A list of dictionaries, each with a 'title' and 'link', 
        or an empty list if the search fails.
    """
    try:
        results = YoutubeSearch(query, max_results=10).to_json()
        results_dict = json.loads(results)
        
        if not results_dict['videos']:
            return []

        video_details = []
        for video in results_dict['videos']:
            video_details.append({
                "title": video['title'],
                "link": f"https://www.youtube.com{video['url_suffix']}"
            })
        return video_details
    except Exception as e:
        print(f"An error occurred during YouTube search: {e}")
        return []

@tool
def get_transcript(video_url: str) -> str:
    """
    Retrieves the full transcript of a YouTube video.

    Args:
        video_url: The URL of the YouTube video.

    Returns:
        The full transcript of the video as a single string, or an empty string if the transcript is disabled or not found.
    """
    if "v=" not in video_url:
        return "Invalid YouTube URL"
    video_id = video_url.split("v=")[1]
    print(f"Extracted video ID: {video_id}")

    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id=video_id)
        transcript = transcript_list.to_raw_data()
        transcript_text = " ".join([item["text"] for item in transcript])
        return transcript_text
    except (TranscriptsDisabled, NoTranscriptFound):
        return "No transcript available for this video."
    except Exception as e:
        return f"An error occurred: {e}"
    