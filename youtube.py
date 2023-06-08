import json
import datetime
from data_handling import responses_to_db
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


CLIENT_SECRETS_FILE = 'scratch/client_secret_45043695667-7cncheujmg27jh9stc3r121jh14qetgi.apps.googleusercontent.com.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_auth_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(
        API_SERVICE_NAME,
        API_VERSION,
        credentials=credentials
    )

# Function used to get all the playlists from the authenticated user.
def list_playlists(youtube):
    list_playlists = youtube.playlists().list(
        part='snippet',
        maxResults=130,
        mine=True
    )
    response = list_playlists.execute()
    clean_json = json.dumps(response)
    with open("pls2.json", "w") as outfile:
        json_load = json.loads(clean_json)
        json.dump(json_load, outfile)

# Helper function used to get all the playlist ids.
def get_playlist_ids():
    with open("pls2.json", "r") as infile:
        data = json.load(infile)
        playlists = data["items"]
        pl_ids = []
        for i in playlists:
            pl_ids.append(i["id"])
    return pl_ids

def save_playlistitems_to_file(youtube, pl_ids):
    print("Adding playlist items to file..")
    datetime_stamp_raw = datetime.datetime.now()
    formatted_datetime_stamp = str(datetime_stamp_raw.strftime('%m-%d-%Y_%H-%M-%S'))
    file_name = str('YouTube-Playlist-Items-' + formatted_datetime_stamp + '.json')
    with open(file_name, "w") as outfile:
        for pl in pl_ids:
            list_playlists_request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=1,
                playlistId=pl
            )
            response = list_playlists_request.execute()
            json.dump(response, outfile)
            print("Continuing..")
    print('Success')

# Function to loop through all the playlist ids, get playlist items (w/ pagination) and pass responses to data handling.
def get_playlist_items(youtube, pl_ids):
    for pl in pl_ids:
        playlistitems_list_request = youtube.playlistItems().list(
            playlistId=pl,
            part="snippet",
            maxResults=50
        )
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()
            responses_to_db(playlistitems_list_response)
            playlistitems_list_request = youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response
            )

# Helper function used to create a file with all the playlist ids.
def make_playlist_file():
    list_playlists(get_auth_service())
    return

if __name__ == '__main__':
    youtube = get_auth_service()
    try:
        list_playlists(youtube)
        get_playlist_items(youtube, pl_ids=get_playlist_ids())
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s') % (e.resp.status, e.content)