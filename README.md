# About

This is an old script that I created in order to migrate my old music files to Spotify. After some refactoring and tests, I decided to publish to help other people that are curious about how to do that or want to learn about how to use Spotipy Python library.

I tested this script against my old MP3 library with more than 6k files and could migrate everything to proper Spotify playlists. 

Please take a look to the script before using, as the script moves the files to categorized folders and if you have problems in your system I won't be responsible for lost files.

# Requirements

* Python 3.6+
* Pip
* [Spotify API Credentials](https://developer.spotify.com/documentation/web-api/)


# How to use

1. Clone the repository and cd to it:

```shell
git clone git@github.com:felipepedroso/mp3tospotify.git
cd mp3tospotify
```

1. Install the required dependencies using `pip`:

```shell
pip install -r requirements.txt
```

1. Create your Spotify Web API app credentials [here](https://developer.spotify.com/documentation/web-api/). 

1. Create the following environment variables using your Spotify credentials:
```shell
export SPOTIFY_CLIENT_ID="<YOUR-CLIENT-ID-HERE>"
export SPOTIFY_CLIENT_SECRET="<YOUR-CLIENT-SECRET-HERE>"
export SPOTIFY_USERNAME="<YOUR-SPOTIFY-USERNAME>"
```

1. Run the script:

```shell
python -m mp3tospotify /path/to/your/mp3/files
```

The script will run and categorize your files into folders according the results of processing.

Please note that you can specify some parameters on the script:

```shell
usage: mp3tospotify [-h] [-p PLAYLIST_NAME] [-m MARKET] path

A simple script to create a Spotify playlist from your old MP3 files.

positional arguments:
  path                  Path to the music files directory.

optional arguments:
  -h, --help            show this help message and exit
  -p PLAYLIST_NAME, --playlist PLAYLIST_NAME
                        The name of the playlist the will be created on
                        Spotify.
  -m MARKET, --market MARKET
                        The market where the track should be available. This
                        should be specified as ISO 3166-1 alpha-2 country
                        code.
```