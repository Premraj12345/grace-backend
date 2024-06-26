# @title Appwrite Code

import re
from appwrite.client import Client
from appwrite.services.databases import Databases
from time import sleep
from pytube import YouTube
import os
from ytmusicapi import YTMusic
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from youtubesearchpython import VideosSearch
import random

def create_id(id,unique_id,track_id):
  client = Client()

  (client
    .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
    .set_project('grace-cron') # Your project ID
    .set_key('e395ed05a7351d4f6dad840eca954a53c8fd713add863af127ba7d5c524c9b7fb85f4cf1cc8e6e9b2665ea0337abfa0e05cb6ccebb6a5e44801fab8d8f2368d3426adef6b00ba6c597d4a011acf05f424640a79af4c18c39a01370df644471759dda7a0c1059748556b3597aecc640235d9d7983877642ac89174c2bd840e63f') # Your secret API key
  )

  databases = Databases(client)

  data = {
      "file-id":id,
      "file-unique-id": unique_id,
      "track-id": track_id
  }

  result = databases.create_document('grace-data', 'ids',document_id=track_id, data=data)


def download_directly(video_url, custom_title):
    output_path = os.getcwd()  # Use the current working directory as the output path
    #custom_title = "".join(c for c in custom_title if c.isalnum() or c in ('.', '-'))  # Remove invalid characters
    output_audio_file = os.path.join(output_path, f"{custom_title}")  # Added file extension

    yt = YouTube(video_url)
    audio_stream_low_mb = yt.streams.filter(only_audio=True).first()
    audio_stream_high_mb = yt.streams.filter(only_audio=True).last()
    audio_stream_high_mb.download(output_path=output_path, filename=f"{custom_title}")  # Use filename argument correctly

    return output_audio_file


def get_video_id(link):
    # Find the index of "v=" in the URL
    index = link.find("v=")

    if index != -1:
        # Extract characters after "v="
        video_id = link[index + 2:]
        return video_id
    else:
        return None

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
      "image_url" : image_url,
      "language": "Telugu"
  }
  result = databases.create_document('gracedb', 'artists', document_id, data)




def create_album(document_id, name, year, artworkurl, artist_id, album_type, artistimageurl,artistname):
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
      "artist": artist_id,
      "type": album_type,
      "artistid": artist_id,
      "artistimageurl": artistimageurl,
      "artistname" : artistname
  }

  result = databases.create_document('gracedb', 'albums', document_id, data)



def create_song(document_id, name, language, length, audiourl, album_id ,album_image_url, artist_name, artistimageurl, albumname, albumyear,albumtype,artistid,file_id):
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
      "album" : album_id,
      "albumartwork":album_image_url,
      "albumartistname" : artist_name,
      "albumid": album_id,
      "artistid": artistid,
      "artistimageurl": artistimageurl,
      "albumname": albumname,
      "albumyear":albumyear ,
      "albumtype": albumtype,
      "file_id":file_id
  }
  result = databases.create_document('gracedb', 'songs', document_id, data)



# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6361645598:AAF8Lioo2hS7tsGPXT0bTn5uT9pGF0gMAB8'


url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
headers = {"accept":"application/json"}


def upload_audio_and_get_link(audio_path, track_document_id, track_name, track_duration_ms, album_document_id ,album_image_url, artist_name,artistimageurl,albumname,albumyear,albumtype,artistid):
  # Replace 'YOUR_CHAT_ID' with the chat ID where you want to send the audio
  chat_id = '1876292868'

  # Replace 'audio_path' with the path to your music/audio file
  audio_path = audio_path

  data = {"chat_id":"1876292868"}


  # Upload the audio file and get the file ID
  with open(audio_path, 'rb') as audio_file:
    files = {"audio": audio_file}
    try:
      resp = requests.post(url, headers=headers, params=data, files=files)
    except:
      return 'Failed'
    resp = resp.json()
    # Extract file_id
    file_id = resp['result']['audio']['file_id']
    audio_file_id = file_id
    unique_id = resp['result']['audio']['file_unique_id']


  #url2 = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={audio_file_id}"
  #file_info = requests.get(url2).json()
  #file_path = file_info['result']['file_path']

  # Step 2: Construct the direct link
  #file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
  file_url = f"https://grace-teleserver.onrender.com/stream/{audio_file_id}"
  language = "Telugu"
  track_duration_ms = str(track_duration_ms)
  create_song(track_document_id,track_name,language,track_duration_ms,file_url,album_document_id,album_image_url, artist_name,artistimageurl,albumname,albumyear,albumtype,artistid,file_id)
  create_id(file_id,unique_id,track_document_id)
  os.system(f'rm "{audio_path}"')
  print('deleted')
  sleep(1)


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

    while True:
      try:
        response = requests.get(ODESLI_API_URL, params=odesli_params)

        if response.text:
          odesli_data = response.json()
          return odesli_data
        else:
          sleep(7)
          continue
      except:
        continue

    return odesli_data

def search_youtube_video(track_name, artist_name):
    query = f"{track_name} {artist_name}"
    video_search = VideosSearch(query, limit = 1)

    results = video_search.result()
    if results['result']:
        return results['result'][0]['link']
    else:
        return 'N/A'

def search_youtube_music(track_name, artist_name):
    ytmusic = YTMusic()

    # Use the search method of the YTMusic API
    results = ytmusic.search(f"{track_name} {artist_name}", filter="songs", limit=1)

    if results:
        # Extract the first result's videoId
        video_id = results[0]['videoId']

        # Create the YouTube Music video link
        return f"https://music.youtube.com/watch?v={video_id}"
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

    artist_name_without_dash = artist_name.replace('-', '')

    artist_name_without_commas = artist_name_without_dash.replace(',', '')
    rand = random.randint(1,99)
    artist_document_id = artist_name_without_commas.replace(" ", "")+str(rand)
    create_artist(artist_document_id, artist_name, artist_image_url)

    print(f"Artist: {artist_name}")
    print(f"Artist Image URL: {artist_image_url}")

    # Get all albums for the artist
    albums = sp.artist_albums(artist_id, limit=50)

    for album in albums['items']:
        album_name = album['name']
        album_id = album['id']
        album_type = album['album_type']
        album_year = album['release_date'].split('-')[0] if 'release_date' in album else 'N/A'
        album_images = album['images'] if 'images' in album else []
        album_image_url = album_images[0]['url'] if album_images else 'N/A'

        album_name_without_dash = album_name.replace('-', '')

        album_name_without_commas = album_name_without_dash.replace(',', '')
        rand = random.randint(1,99)
        album_document_id = album_name_without_commas.replace(" ", "")+str(rand)
        create_album(album_document_id,album_name,album_year,album_image_url,artist_document_id,album_type,artist_image_url,artist_name)

        print(f"\nAlbum: {album_name}, Year: {album_year}")
        print(f"Album Image URL: {album_image_url}")

        # Get all tracks for the album
        tracks = sp.album_tracks(album_id)

        for track in tracks['items']:
            track_name = track['name']
            track_duration_ms = track['duration_ms']
            track_audio_url = track['preview_url'] if 'preview_url' in track else 'N/A'

            track_name_without_dash = track_name.replace('-', '')

            track_name_without_commas = track_name_without_dash.replace(',', '')
            rand = random.randint(1,99)
            track_without_space = track_name_without_commas.replace(" ", "")+str(rand)
            track_document_id = ''.join(char for char in track_without_space if char not in '()')

            print(f"  Track: {track_name}, Duration: {track_duration_ms} ms")
            print(f"  Audio URL: {track_audio_url}")

            # Get Spotify track link and Odesli info
            spotify_track_link = track['external_urls']['spotify']
            odesli_info = get_odesli_info(spotify_track_link)

            # Get YouTube Music or YouTube link
            youtube_music_link = odesli_info['links']['youtubeMusic']['url'] if 'youtubeMusic' in odesli_info['links'] else 'N/A'
            youtube_link = odesli_info['links']['youtube']['url'] if 'youtube' in odesli_info['links'] else 'N/A'
            youtube_music_link_from_ytmusic = search_youtube_music(track_name, artist_name)
            youtube_video_link_from_yt = search_youtube_video(track_name,artist_name)

            print(f"  YouTube Music Link: {youtube_music_link}")
            print(f"  YouTube Link: {youtube_link}")
            print(f"  YouTube Music Link From YTMusic: {youtube_music_link_from_ytmusic}")
            print(f"  YouTube Video Link From YT: {youtube_video_link_from_yt}")

            only_youtube_music_links = [youtube_music_link,youtube_link,youtube_music_link_from_ytmusic]

            youtube_links = [youtube_music_link,youtube_link,youtube_music_link_from_ytmusic,youtube_video_link_from_yt]

            #download audio
            for yt in youtube_links:
              try:
                filepath = track_name+'-'+ get_video_id(yt)+'.m4a'
                download_directly(yt,filepath)
                print('pytube donloaded')
                sleep(3)
                break
              except:
                try:
                  filepath = track_name+'-'+ get_video_id(yt)+'.m4a'
                  os.system(f'youtube-dl {yt} --extract-audio --audio-format m4a --audio-quality 128K')
                  sleep(3)
                  break
                except:
                  continue

            for i in range(3):
              try:
                result = upload_audio_and_get_link(filepath, track_document_id, track_name, track_duration_ms, album_document_id,album_image_url, artist_name, artist_image_url,album_name, album_year, album_type,artist_document_id)
                if result == 'Failed':
                  pass
                  print('failed')
                break
              except:
                print("upload_audio_and_get_link not did correctly")
                sleep(3)
                continue

            '''
                for link in youtube_links:
                  try:
                    filepath = track_name+'-'+ get_video_id(link)+'.m4a'
                    os.system(f'youtube-dl {link} --extract-audio --audio-format m4a --audio-quality 128K')
                    result = upload_audio_and_get_link(filepath, track_document_id, track_name, track_duration_ms, album_document_id,album_image_url, artist_name, artist_image_url,album_name, album_year, album_type,artist_document_id)
                    if result == 'Failed':
                      continue
                    break
                  except:
                    continue'''


if __name__ == "__main__":
    #get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, ARTIST_ID)
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "1wAnjuaT1lZ9ULjRJIq3rX")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "1XaWLxLjDeXKZx4LmHsQQf")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "3jUK1cBOUowwrQ4PGbRLFs")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "15iXlII4LWR2fHDLZ4dAow")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "0n9FqtIMcQl07VxdqpYVml")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "5pCZk4EhxyQ17HZS5Vom2e")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "6xVtWyCifA1UVXCTeGQdSh")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "42LJGLdvmjG2teUzhLkV48")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "2ZI6RrNaij9iVXKcV6kgsv")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "3nr5yEkaBmm6tVAgiuCr7W")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "5imstv16Uz57btzlivDf9d")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "4Kr0VfCRfzrL9WNgDe4tKT")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "4RFBVzwwslm0sfk08PjKZE")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "2A5Yv7UZM3yo9zAR7wTfRh")
    get_artist_albums_and_songs(CLIENT_ID, CLIENT_SECRET, "24AVVNtLGzMlgVS5UIPWH6")
