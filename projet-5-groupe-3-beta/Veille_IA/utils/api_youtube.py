from urllib.request import urlopen
from json import loads
from re import search
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_metadata(url):
    """ Return metadata for a given YouTube video URL.

    Args:
        url (str): YouTube video URL

    Returns:
        dict: Metadata for the video
    """

    # Get the video ID from the URL
    video_id = search(r'v=([^&]+)', url).group(1)

    # Get the metadata from YouTube
    api_url = 'https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=snippet,contentDetails,statistics,status'.format(video_id, 'AIzaSyD5N13DOTzFdd15pgxbglIlBa2mLqB3Ig0')
    response = urlopen(api_url)
    data = loads(response.read().decode('utf-8'))

    # Get the video's metadata
    metadata = {
        'title': data['items'][0]['snippet']['title'],
        'description': data['items'][0]['snippet']['description'],
        'tags': data['items'][0]['snippet']['tags'],
        'category_id': data['items'][0]['snippet']['categoryId'],
    }
    return metadata

