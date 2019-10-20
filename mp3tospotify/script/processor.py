from os import listdir, mkdir
from os.path import isfile, join, exists, isdir
from sys import exit
import shutil
from tinytag import TinyTag
import re
from ..utils.fileutils import ensure_folder_existence, move_file
from ..spotify.spotifyapimanager import SpotifyApiManager
from ..utils.musicfiles import is_valid_music_file

_FOLDER_FAILED_READING = "FailedToReadTracks"
_FOLDER_TRACKS_NOT_FOUND = "TracksNotFound"
_FOLDER_ADDED_TRACKS = "AddedTracks"
_FOLDER_DUPLICATED_TRACKS = "DuplicatedTracks"
_FOLDER_FAILED_TO_ADD_TO_PLAYLIST = "FailedToAddToPlaylist"
_DEFAULT_PLAYLIST_NAME = "My Old Music Files"


def _ensure_result_folder_exists(musics_directory, folder_name):
    result_folder_path = join(musics_directory, folder_name)
    ensure_folder_existence(result_folder_path)


def _move_to_result_folder(musics_directory, folder_name, file_path):
    _ensure_result_folder_exists(musics_directory, folder_name)
    result_folder_path = join(musics_directory, folder_name)
    move_file(file_path, result_folder_path)


def _move_file_to_added_folder(musics_directory, file_path):
    _move_to_result_folder(musics_directory, _FOLDER_ADDED_TRACKS, file_path)


def _move_file_to_added_folder(musics_directory, file_path):
    _move_to_result_folder(musics_directory, _FOLDER_ADDED_TRACKS, file_path)


def _move_file_to_not_found_folder(musics_directory, file_path):
    _move_to_result_folder(
        musics_directory, _FOLDER_TRACKS_NOT_FOUND, file_path)


def _move_file_to_cannot_read_folder(musics_directory, file_path):
    _move_to_result_folder(musics_directory, _FOLDER_FAILED_READING, file_path)


def _move_file_to_duplicated_folder(musics_directory, file_path):
    _move_to_result_folder(
        musics_directory, _FOLDER_DUPLICATED_TRACKS, file_path)

def _move_file_to_playlist_fail_folder(musics_directory, file_path):
    _move_to_result_folder(
        musics_directory, _FOLDER_FAILED_TO_ADD_TO_PLAYLIST, file_path)


def process_folder(musics_directory, playlist_name, market=None, tracks_batch_size=10):
    if not isdir(musics_directory):
        print("Cannot find the musics folder.")
        exit()

    files = listdir(musics_directory)

    if len(files) <= 0:
        print("The musics folder is empty.")
        exit()

    spotify_api_manager = SpotifyApiManager()

    playlist_id = spotify_api_manager.create_or_get_playlist(
        playlist_name or _DEFAULT_PLAYLIST_NAME)

    tracks_dictionary = dict()
    added_ids = set()

    for index, file in enumerate(files):
        file_path = join(musics_directory, file)

        if is_valid_music_file(file_path):
            artist = None
            title = None
            try:
                audio_tag = TinyTag.get(file_path)
                artist = audio_tag.artist
                title = re.sub(r'\(\d\d\d\d\)', '', audio_tag.title)
            except:
                print('Failed to parse \'%s\'' % file_path)
                _move_file_to_cannot_read_folder(musics_directory, file_path)
                continue

            if(not artist is None and not title is None):
                best_track_id = None
                
                try:
                    best_track_id = spotify_api_manager.get_track_id(title, artist, market)
                except:
                    best_track_id = None

                if best_track_id is None:
                    print('Couldn\'t find \'%s\' on Spotify.' % file_path)
                    _move_file_to_not_found_folder(musics_directory, file_path)
                    continue
                elif best_track_id not in added_ids:
                    added_ids.add(best_track_id)
                    tracks_dictionary[best_track_id] = file_path
                else:
                    _move_file_to_duplicated_folder(
                        musics_directory, file_path)

            else:
                print('Invalid artist or name')
                continue

        if len(tracks_dictionary) >= tracks_batch_size or index == len(files) - 1:
            music_ids_to_add = list(tracks_dictionary.keys())

            try:
                spotify_api_manager.add_tracks_to_playlist(
                    playlist_id, music_ids_to_add)
            except:
                for key in tracks_dictionary:
                    _move_file_to_playlist_fail_folder(
                    musics_directory, tracks_dictionary[key])
                    tracks_dictionary.clear()
                    continue

            for key in tracks_dictionary:
                _move_file_to_added_folder(
                    musics_directory, tracks_dictionary[key])

            tracks_dictionary.clear()

    print('Done!')
