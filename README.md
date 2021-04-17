# Twitch Clip Youtuber

Automatically download an amount of Twitch Clips, put them together as one video and upload it to Youtube


# Installation

- Run `pip install -r requirements.txt`
- Register for Twitch Api and set `CLIENT_ID = '<TWITCH_API_CLIENT_ID>'` and `CLIENT_SECRET = '<TWITCH_API_CLIENT_SECRET>'`
- Create a Google Api Project and OAuth2 credentials
- Create `yt_client_secret.json` and add OAuth2 credentials
- Change game name and amount of clips to your liking in the call to `get_twitch_clip('Among Us', 3)`
- Run the script

# Known Issues

- Basically no error handling
- Does not work with more than 4 clips (Does not handle pagination from Twitch Api)
- Youtube video title and description are hardcoded
- If Google Api Service is not verified, upload will only produce private Youtube videos