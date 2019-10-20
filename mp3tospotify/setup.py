from setuptools import setup

setup(name='mp3tospotify',
      version='0.5',
      description='A simple script to send your old music files to a Spotify playlist.',
      author='Felipe Pedroso',
      author_email='f.pedroso677@gmail.com',
      license='MIT',
      package='mp3tospotify',
      install_requires=[
          'tinytag',
          'spotipy'
      ],
      zip_safe=False)
      
