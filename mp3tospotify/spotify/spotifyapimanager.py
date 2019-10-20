from os import environ
from ..utils.constants import CLIENT_ID_ENV_VAR, CLIENT_SECRET_ENV_VAR, USERNAME_ENV_VAR, SPOTIFY_API_SCOPE, DEFAULT_REDIRECT_URL
from ..utils.environmentvars import get_environment_variable
import spotipy
import spotipy.util as util

_ITEMS_FIELD = 'items'
_NAME_FIELD = 'name'
_ID_FIELD = 'id'
_TRACKS_FIELD = 'tracks'
_AVAILABLE_MARKETS_FIELD = 'available_markets'
_TYPE_TRACK = 'track'


class SpotifyApiManager:

    def __init__(self):
        client_id = get_environment_variable(CLIENT_ID_ENV_VAR)
        client_secret = get_environment_variable(CLIENT_SECRET_ENV_VAR)
        self.username = get_environment_variable(USERNAME_ENV_VAR)
        token = util.prompt_for_user_token(self.username, SPOTIFY_API_SCOPE, client_id=client_id,
                                           client_secret=client_secret, redirect_uri=DEFAULT_REDIRECT_URL)
        self.spotify = spotipy.Spotify(token)

    def get_playlists(self):
        return self.spotify.user_playlists(self.username)[_ITEMS_FIELD]

    def create_playlist(self, playlist_name):
        return self.spotify.user_playlist_create(user=self.username, name=playlist_name, public=False)

    def create_or_get_playlist(self, playlist_name):
        user_playlists = self.get_playlists()

        playlists_with_selected_name = list(
            filter(lambda playlist: playlist[_NAME_FIELD] == playlist_name, user_playlists))

        playlist = None

        if len(playlists_with_selected_name) > 0:
            playlist = playlists_with_selected_name[0]
        else:
            playlist = self.create_playlist(playlist_name)

        if playlist is None:
            print(
                'Failed to create the playlist. PLease check if you have connectivity or the Spotify credentials are working properly.')
            exit()

        return playlist[_ID_FIELD]

    def get_track_id(self, title, artist, market=None):
        query = 'track:' + title.lower() + " artist:" + artist.lower()

        result = self.spotify.search(q=query, type=_TYPE_TRACK)

        result_items = result[_TRACKS_FIELD][_ITEMS_FIELD]

        if market is not None:
            result_items = list(filter(
                lambda element: market in element[_AVAILABLE_MARKETS_FIELD], result_items))

        best_track_id = None

        results_count = len(result_items)

        print(str(results_count) + ' Results for \'' +
              artist + ' - ' + title + '\': ' + str(results_count))

        if results_count > 0:
            best_track_id = result_items[0][_ID_FIELD]

        return best_track_id

    def add_tracks_to_playlist(self, playlist_id, tracks_ids):
        self.spotify.user_playlist_add_tracks(self.username, playlist_id, tracks_ids)
