import argparse
from .script.processor import process_folder

parser = argparse.ArgumentParser(
    prog='mp3tospotify', description='A simple script to create a Spotify playlist from your old MP3 files.')

parser.add_argument(
    'path',
    metavar='path',
    type=str,
    help='Path to the music files directory.'
)

parser.add_argument(
    '-p', 
    '--playlist', 
    dest='playlist_name',
    type=str,
    help='The name of the playlist the will be created on Spotify.'
)

parser.add_argument(
    '-m', 
    '--market', 
    dest='market',
    type=str,
    help='The market where the track should be available. This should be specified as ISO 3166-1 alpha-2 country code.'
)

args = parser.parse_args()

process_folder(args.path, args.playlist_name, args.market)
