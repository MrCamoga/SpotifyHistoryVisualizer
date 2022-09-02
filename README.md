# SpotifyHistoryVisualizer
Visualize your spotify listening history.

Download your past year's data or your full history from [here](https://www.spotify.com/us/account/privacy/).

# Usage
Copy your JSON files to the data directory and run the python code. You can combine files of different history requests as the program automatically removes duplicate songs.

# Functions

## Plots
- plotTotalMinutes: total minutes listened
- plotArtistMinutes: total minutes of one artist 
- plotTopArtists: total minutes of top artists
- plotTopSongs: total minutes of top songs
- plotTopSongsArtists: total minutes of top songs by one artist
- plotHour: total minutes listened each hour of the day
- plotMinute: total minutes listened each minute of the day

## Calendar plots
TODO: add artist/song legend

- calplotTopArtists: top artist of each day
- calplotTopSongs: top song of each day
- calplotTotalMinutes: total minutes listened each day
- calplotTotalCount: total number of songs listened each day
- calplotArtistMinutes: total minutes listened of one artist