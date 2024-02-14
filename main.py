import re
from appwrite.client import Client
from appwrite.services.databases import Databases

def get_video_id(link):
  url = link

  # Use a regular expression to extract the video ID
  match = re.search(r"youtube\.com/watch\?v=([a-zA-Z0-9_-]+)", url)

  if match:
      video_id = match.group(1)
      return video_id
  else:
      return 1

def create_artist(document_id, name, image_url):
  client = Client()

  (client
    .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
    .set_project('grace') # Your project ID
    .set_key('e266f306b413e0b804585c09970b8ebb64bfda39f7029200dfd1e13f4bc30cce936ab2bb35b328714de578591d9fc60d79e7f4406c6fe61591bdec3c49375cb2f7f14d92110ba16811d9680318d3894397e01336b132a4913eb02497eaf3945a5221d5e6685f019f96cd51d3a2a3f3d5b6b02437a3619a42fefe5daee76fa1be') # Your secret API key
  )

  databases = Databases(client)

  data = {
      "name": name,
      "image_url" : image_url
  }
  result = databases.create_document('gracedb', 'artists', document_id, data)




def create_album(document_id, name, year, artworkurl, artist_id):
  client = Client()

  (client
    .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
    .set_project('grace') # Your project ID
    .set_key('e266f306b413e0b804585c09970b8ebb64bfda39f7029200dfd1e13f4bc30cce936ab2bb35b328714de578591d9fc60d79e7f4406c6fe61591bdec3c49375cb2f7f14d92110ba16811d9680318d3894397e01336b132a4913eb02497eaf3945a5221d5e6685f019f96cd51d3a2a3f3d5b6b02437a3619a42fefe5daee76fa1be') # Your secret API key
  )

  databases = Databases(client)

  data = {
      "name": name,
      "year": year,
      "artworkurl": artworkurl,
      "artist": artist_id
  }

  result = databases.create_document('gracedb', 'albums', document_id, data)



def create_song(document_id, name, language, length, audiourl, album_id):
  client = Client()

  (client
    .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
    .set_project('grace') # Your project ID
    .set_key('e266f306b413e0b804585c09970b8ebb64bfda39f7029200dfd1e13f4bc30cce936ab2bb35b328714de578591d9fc60d79e7f4406c6fe61591bdec3c49375cb2f7f14d92110ba16811d9680318d3894397e01336b132a4913eb02497eaf3945a5221d5e6685f019f96cd51d3a2a3f3d5b6b02437a3619a42fefe5daee76fa1be') # Your secret API key
  )

  databases = Databases(client)

  data = {
      "name": name,
      "language" : language,
      "audiourl" : audiourl,
      "album" : album_id
  }
  result = databases.create_document('gracedb', 'songs', document_id, data)






import nest_asyncio
nest_asyncio.apply()

import asyncio
from telegram import Bot, InputFile

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6361645598:AAF8Lioo2hS7tsGPXT0bTn5uT9pGF0gMAB8'
bot = Bot(token=bot_token)

async def upload_audio_and_get_link(audio_path, track_document_id, track_name, track_duration_ms, album_document_id ):
    # Replace 'YOUR_CHAT_ID' with the chat ID where you want to send the audio
    chat_id = '1876292868'

    # Replace 'audio_path' with the path to your music/audio file
    audio_path = audio_path

    # Upload the audio file and get the file ID
    with open(audio_path, 'rb') as audio_file:
        audio_message = await bot.send_audio(chat_id, audio=audio_file)
        audio_file_id = audio_message.audio.file_id

    # Step 1: Get the file path using getFile API
    file_info = await bot.get_file(audio_file_id)
    file_path = file_info.file_path

    # Step 2: Construct the direct link
    file_url = file_path
    language = "Telugu"
    track_duration_ms = str(track_duration_ms)
    create_song(track_document_id,track_name,language,track_duration_ms,file_url,album_document_id)

# Create and run the event loop
#loop = asyncio.get_event_loop()
#loop.run_until_complete(upload_audio_and_get_link())





import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from youtubesearchpython import VideosSearch
import os

import random

CLIENT_ID = '809f33d70a1c41a5a060b9686f953036'
CLIENT_SECRET = 'ffb68d777ada430c90aff2ebdc217075'
ARTIST_ID = '1TydqAcoTSPSM8UT9JW8Fz'

ODESLI_API_URL = 'https://api.odesli.co/matches'

def get_odesli_info(spotify_track_link):
    odesli_params = {
        'url': spotify_track_link,
        'songIfSingle': 'true',
        'userCountry': 'IN'
    }

    response = requests.get(ODESLI_API_URL, params=odesli_params)
    odesli_data = response.json()

    return odesli_data

def search_youtube_video(track_name, artist_name):
    query = f"{track_name} {artist_name} official video"
    video_search = VideosSearch(query, limit = 1)

    results = video_search.result()
    if results['result']:
        return results['result'][0]['link']
    else:
        return 'N/A'

def get_artist_albums_and_songs(client_id, client_secret, artist_id):
    # Set up Spotify API client
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get artist details
    artist = sp.artist(artist_id)
    artist_name = artist['name']
    artist_images = artist['images'] if 'images' in artist else []
    artist_image_url = artist_images[0]['url'] if artist_images else 'N/A'

    rand = random.randint(1,99)
    artist_document_id = artist_name.replace(" ", "")+str(rand)
    create_artist(artist_document_id, artist_name, artist_image_url)

    print(f"Artist: {artist_name}")
    print(f"Artist Image URL: {artist_image_url}")

    # Get all albums for the artist
    albums = sp.artist_albums(artist_id, album_type='album', limit=50)

    for album in albums['items']:
        album_name = album['name']
        album_id = album['id']
        album_year = album['release_date'].split('-')[0] if 'release_date' in album else 'N/A'
        album_images = album['images'] if 'images' in album else []
        album_image_url = album_images[0]['url'] if album_images else 'N/A'

        rand = random.randint(1,99)
        album_document_id = album_name.replace(" ", "")+str(rand)
        create_album(album_document_id,album_name,album_year,album_image_url,artist_document_id)

        print(f"\nAlbum: {album_name}, Year: {album_year}")
        print(f"Album Image URL: {album_image_url}")

        # Get all tracks for the album
        tracks = sp.album_tracks(album_id)

        for track in tracks['items']:
            track_name = track['name']
            track_duration_ms = track['duration_ms']
            track_audio_url = track['preview_url'] if 'preview_url' in track else 'N/A'

            rand = random.randint(1,99)
            track_document_id = track_name.replace(" ", "")+str(rand)

            print(f"  Track: {track_name}, Duration: {track_duration_ms} ms")
            print(f"  Audio URL: {track_audio_url}")

            # Get Spotify track link and Odesli info
            spotify_track_link = track['external_urls']['spotify']
            odesli_info = get_odesli_info(spotify_track_link)

            # Get YouTube Music or YouTube link
            youtube_music_link = odesli_info['links']['youtubeMusic']['url'] if 'youtubeMusic' in odesli_info['links'] else 'N/A'
            youtube_link = odesli_info['links']['youtube']['url'] if 'youtube' in odesli_info['links'] else 'N/A'

            print(f"  YouTube Music Link: {youtube_music_link}")
            print(f"  YouTube Link: {youtube_link}")

            # Search for the video on YouTube and get the link
            youtube_video_link = search_youtube_video(track_name, artist_name)
            print(f"  YouTube Video Link: {youtube_video_link}")

            if len(youtube_music_link) > 9:
              filepath = track_name+'-'+ get_video_id(youtube_music_link)+'.m4a'
              os.system(f'youtube-dl {youtube_music_link} --extract-audio --audio-format m4a --audio-quality 128K')
              loop = asyncio.get_event_loop()
              loop.run_until_complete(upload_audio_and_get_link(filepath, track_document_id, track_name, track_duration_ms, album_document_id ))
            elif len(youtube_link) > 9:
              filepath = track_name+'-'+ get_video_id(youtube_link)+'.m4a'
              os.system(f'youtube-dl {youtube_link} --extract-audio --audio-format m4a --audio-quality 128K')
              loop = asyncio.get_event_loop()
              loop.run_until_complete(upload_audio_and_get_link(filepath, track_document_id, track_name, track_duration_ms, album_document_id ))

            else:
              filepath = track_name+'-'+ get_video_id(youtube_video_link)+'.m4a'
              os.system(f'youtube-dl {youtube_video_link} --extract-audio --audio-format m4a --audio-quality 128K')
              loop = asyncio.get_event_loop()
              loop.run_until_complete(upload_audio_and_get_link(filepath, track_document_id, track_name, track_duration_ms, album_document_id ))



if __name__ == "__main__":
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, ARTIST_ID)
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "1wAnjuaT1lZ9ULjRJIq3rX")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "1XaWLxLjDeXKZx4LmHsQQf")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "1w8S83yGWdb6sN3s6mjg28")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "02m3PiiWBO9hWspWxZqB7k")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "7zRvtToaWinJSv96cbx3YU")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "3jUK1cBOUowwrQ4PGbRLFs")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "15iXlII4LWR2fHDLZ4dAow")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "0n9FqtIMcQl07VxdqpYVml")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "5pCZk4EhxyQ17HZS5Vom2e")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "6xVtWyCifA1UVXCTeGQdSh")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "42LJGLdvmjG2teUzhLkV48")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "2ZI6RrNaij9iVXKcV6kgsv")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "3nr5yEkaBmm6tVAgiuCr7W")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "5imstv16Uz57btzlivDf9d")
