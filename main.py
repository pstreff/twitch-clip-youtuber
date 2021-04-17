import shutil
import urllib
import uuid
from datetime import datetime

from googleapiclient.http import MediaFileUpload
from moviepy.editor import *

import requests

from Google import create_service

DOMAIN = 'https://api.twitch.tv/'
CLIENT_ID = '<TWITCH_API_CLIENT_ID>'
CLIENT_SECRET = '<TWITCH_API_CLIENT_SECRET>'
YOUTUBE_CLIENT_SECRET_FILE = 'yt_client_secret.json'


# TODO: implement second method using Get Top Clips endpoint
def get_twitch_clip(game_name, number_of_clips=1):
    url = DOMAIN + 'helix/clips'

    token = get_access_token()  # TODO: cache token

    headers = {'Client-ID': CLIENT_ID, 'Authorization': 'Bearer ' + token}

    game_id = get_game_id(game_name)

    # get current date in RFC3339 format
    started_at = datetime.utcnow().isoformat("T").split('.')[0] + 'Z'

    r = requests.get(url + '?game_id=' + game_id + '&first=' + str(number_of_clips) + '&started_at=' + started_at, headers=headers)

    for i in range(len(r.json()['data'])):
        clip_preview_url = r.json()['data'][i]['thumbnail_url']

        clip_download_url = clip_preview_url.split('-preview', 1)[0] + '.mp4'

        if not os.path.exists('clips'):
            os.makedirs('clips')

        filename = os.path.join('clips', str(uuid.uuid4()) + '.mp4')

        try:
            urllib.request.urlretrieve(clip_download_url, filename)
        except Exception as e:
            print('Error')
            print(e)


def get_game_id(game_name):
    url = DOMAIN + 'helix/games?name=' + game_name

    token = get_access_token()

    headers = {'Client-ID': CLIENT_ID, 'Authorization': 'Bearer ' + token}

    r = requests.get(url, headers=headers)

    return r.json()['data'][0]['id']


def get_access_token():
    # TODO: cache token
    r = requests.post('https://id.twitch.tv/oauth2/token?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + '&grant_type=client_credentials')

    return r.json()['access_token']


def create_youtube_video():
    clips = []
    for clip in [os.path.join('clips', f) for f in os.listdir('clips') if os.path.isfile(os.path.join('clips', f))]:
        clips.append(VideoFileClip(clip))

    final = concatenate_videoclips(clips)

    final.write_videofile('final.mp4')


def youtube_upload():
    scopes = ['https://www.googleapis.com/auth/youtube.upload']

    service = create_service(YOUTUBE_CLIENT_SECRET_FILE, 'youtube', 'v3', scopes)

    request_body = {
        'snippet': {
            'title': 'Demo | Automated Among Us Twitch Clips',
            'description': 'Demo Automated Twitch Clips to Youtube'
        },
        'status': {
            'privacyStatus': 'unlisted'
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload('final.mp4')

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    print(response_upload)


def main():
    if os.path.exists('clips'):
        shutil.rmtree('clips')

    get_twitch_clip('Among Us', 3)

    create_youtube_video()

    youtube_upload()


if __name__ == '__main__':
    main()
