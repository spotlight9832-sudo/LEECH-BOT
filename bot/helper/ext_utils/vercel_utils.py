import aiohttp
import json
from bot import config_dict, LOGGER

async def generate_vercel_links(video_url: str, title: str, poster_url: str = "", subtitles: list = None, audio_tracks: list = None):
    """
    Calls the Vercel API to generate watch and download links for the Stream Mod.

    Args:
        video_url: The URL of the video (e.g., Telegram file download link)
        title: The title of the video
        poster_url: The URL to the thumbnail/poster image
        subtitles: A list of dicts [{"src": "...", "lang": "en", "label": "English"}]
        audio_tracks: A list of dicts [{"src": "...", "lang": "en", "label": "English"}]

    Returns:
        tuple: (watch_link, download_link) or (None, None) on failure.
    """
    vercel_url = config_dict.get('VERCEL_URL')
    vercel_api = config_dict.get('VERCEL_API')

    if not vercel_url or not vercel_api:
        LOGGER.warning("VERCEL_URL or VERCEL_API is not set in config.")
        return None, None

    endpoint = f"{vercel_url.rstrip('/')}/api/generate"

    payload = {
        "video_url": video_url,
        "title": title,
        "poster_url": poster_url,
        "subtitles": subtitles or [],
        "audio_tracks": audio_tracks or []
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {vercel_api}" # Assuming standard Bearer token Auth, adjust if custom.
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        links = data.get("data", {})
                        watch_link = links.get("watch_link")
                        download_link = links.get("download_link")
                        return watch_link, download_link
                    else:
                        LOGGER.error(f"Vercel API returned failure: {data.get('message')}")
                else:
                    LOGGER.error(f"Vercel API HTTP Error: {response.status} - {await response.text()}")
    except Exception as e:
        LOGGER.error(f"Error calling Vercel API: {e}")

    return None, None
