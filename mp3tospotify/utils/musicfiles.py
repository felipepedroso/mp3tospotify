from os.path import isfile

mp3_file_extension = ".mp3"
wma_file_extension = ".wma"
ogg_file_extension = ".ogg"

def is_valid_music_file(file_path):
    lower_file_path = file_path.lower()

    is_mp3 = lower_file_path.endswith(mp3_file_extension)
    is_wma = lower_file_path.endswith(wma_file_extension)
    is_ogg = lower_file_path.endswith(ogg_file_extension)

    return isfile(file_path) and (is_mp3 or is_wma or is_ogg)