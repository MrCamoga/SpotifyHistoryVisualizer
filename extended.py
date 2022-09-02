import os, json, datetime, re
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
import calplot
import numpy as np

numprint = 10

history = []
ignorerepeats = set()

def readExtendedHistory(datafile):
    global history, ignorerepeats
    with open("data/"+datafile,'r',encoding="utf-8") as file:
        data = json.load(file)
        for song in data:
            artist = song['master_metadata_album_artist_name']
            trackname = song['master_metadata_track_name']
            date = datetime.datetime.strptime(song['ts'],'%Y-%m-%dT%H:%M:%SZ')
            day = str(date.date())
            time = int(song['ms_played'])/60000.0
            if artist is None or time < 0.08:
                continue

            history += [[date,artist,trackname,time]]
            ignorerepeats.add((date.replace(second=0),artist,trackname))

def readYearHistory(datafile):
    global history, ignorerepeats
    with open("data/"+datafile,'r',encoding="utf-8") as file:
        data = json.load(file)
        for song in data:
            artist = song['artistName']
            trackname = song['trackName']
            date = datetime.datetime.strptime(song['endTime'],'%Y-%m-%d %H:%M')
            day = str(date.date())
            time = int(song['msPlayed'])/60000.0
            if artist is None or time < 0.08:
                continue

            #if df[(df["date"].dt.floor("min")==date) & (df["artist"]==artist) & (df["trackname"]==trackname)].empty:
            i = (date.replace(second=0),artist,trackname)
            if i not in ignorerepeats:
                history += [[date,artist,trackname,time]]
                ignorerepeats.add(i)

for datafile in list(filter(lambda x: re.search('endsong_[0-9]*\.json',x),os.listdir("data"))):
    readExtendedHistory(datafile)

for datafile in list(filter(lambda x: re.search('StreamingHistory[0-9]*\.json',x),os.listdir("data"))):
    readYearHistory(datafile)

df = pd.DataFrame(history, columns=['date','artist','trackname','time'])
dfartists = df.groupby('artist')
dfsongs = df.groupby('trackname')

print("Most listened artists (minutes):\n")
print(dfartists.sum().sort_values('time',ascending=False).head(numprint).to_string())
#print(*sorted(list(artists.items()),key=lambda x: -x[1][1])[0:numprint],sep="\n")

print()
print("Most listened artists (count):\n")
print(dfartists.size().sort_values(ascending=False).head(numprint).to_string())
#print(*sorted(list(artists.items()),key=lambda x: -x[1][0])[0:numprint],sep="\n")

print()
print("Most listened songs (minutes):\n")
print(dfsongs.sum().sort_values('time',ascending=False).head(numprint).to_string())
#print(*sorted(list(songs.items()),key=lambda x: -x[1][1])[0:numprint],sep="\n")

print()
print("Most listened songs (count):\n")
print(dfsongs.size().sort_values(ascending=False).head(numprint).to_string())
#print(*sorted(list(songs.items()),key=lambda x: -x[1][0])[0:numprint],sep="\n")

print()
print("Days artist has been the most listened to (count):\n")
print(df.groupby([pd.Grouper(key='date',freq='D'),'artist']).size().groupby(level=0).idxmax().str[1].value_counts().head(numprint).to_string())
#print(*counttopartistday[0:numprint],sep="\n")

print()
print("Days song has been the most listened to (count):\n")
print(df.groupby([pd.Grouper(key='date',freq='D'),'trackname']).size().groupby(level=0).idxmax().str[1].value_counts().head(numprint).to_string())
#print(*counttopsongday[0:numprint],sep="\n")

print()
print("Days artist has been the most listened to (time):\n")
print(df.groupby([pd.Grouper(key='date',freq='D'),'artist']).sum().groupby(level=0).idxmax()['time'].str[1].value_counts().head(numprint).to_string())
#print(*timetopartistday[0:numprint],sep="\n")

print()
print("Days song has been the most listened to (time):\n")
print(df.groupby([pd.Grouper(key='date',freq='D'),'trackname']).sum().groupby(level=0).idxmax()['time'].str[1].value_counts().head(numprint).to_string())
#print(*timetopsongday[0:numprint],sep="\n")



colorpalette = ['#2f4f4f','#8b4513','#808000','#008000','#000080','#9acd32',
'#8fbc8f','#8b008b','#ff0000','#ff8c00','#ffd700','#6a5acd','#7fff00','#9400d3',
'#00fa9a','#dc143c','#00ffff','#00bfff','#0000ff','#d8bfd8','#db7093','#f0e68c',
'#ff1493','#ffa07a'] + ['#ffffff']

def getArtistDayMinutesCumSum(artist):
    return df[df["artist"]==artist].groupby(pd.Grouper(key='date',freq='D')).sum().squeeze().cumsum()

def getSongDayMinutesCumSum(artist,song):
    return df[(df["artist"]==artist) & (df["trackname"]==song)].groupby(pd.Grouper(key='date',freq='D')).sum().squeeze().cumsum()

def plotTotalMinutes():
    series = df.groupby(pd.Grouper(key='date',freq='D')).sum().squeeze().cumsum()
    plt.plot(series)
    plt.show()

def plotArtistMinutes(artist):
    plt.plot(getArtistDayMinutesCumSum(artist),label=artist)
    plt.show()

def plotTopArtists(count=10):
    top = df.groupby('artist').sum().sort_values("time",ascending=False).head(count)
    for artist in top.index:
        plt.plot(getArtistDayMinutesCumSum(artist),label=artist)
    plt.legend()
    plt.ylabel('Minutes')
    plt.xlabel("")
    plt.show()

def plotTopSongs(count=10):
    top = df.groupby(['artist','trackname']).sum().sort_values("time",ascending=False).head(count)
    for song in top.index:
        plt.plot(getSongDayMinutesCumSum(*song),label=song[1])
    plt.legend()
    plt.ylabel('Minutes')
    plt.xlabel("")
    plt.show()

def plotTopSongsArtist(artist,count=20):
    top = df[df['artist']==artist].groupby('trackname').sum().sort_values("time",ascending=False).head(count)
    for song in top.index:
        plt.plot(getSongDayMinutesCumSum(artist,song),label=song)
    plt.legend()
    plt.ylabel('Minutes')
    plt.xlabel("")
    plt.show()

def plotHour(year=None):
    if year is None:
        plt.plot(df.groupby(df['date'].dt.hour).sum())
    else:
        plt.plot(df[df['date'].dt.year==year].groupby(df['date'].dt.hour).sum())
    plt.show()

def plotMinute(year=None):
    if year is None:
        plt.plot(df.groupby(df['date'].dt.minute+60*df['date'].dt.hour).sum())
        plt.plot(df.groupby(60*df['date'].dt.hour).sum().apply(lambda x: x/60))
    else:
        plt.plot(df[df['date'].dt.year==year].groupby(df['date'].dt.minute+60*df['date'].dt.hour).sum())
        plt.plot(df[df['date'].dt.year==year].groupby(60*df['date'].dt.hour).sum().apply(lambda x: x/60))
    plt.show()

def calplotTopArtist(count=10):
    top = df.groupby([pd.Grouper(key='date',freq='D'),'artist']).sum().groupby('date')['time'].idxmax().str[1].value_counts().head(count)
    d = {a:i+1 for i,a in enumerate(top.keys())}
    series = df.groupby([pd.Grouper(key='date',freq='D'),'artist']).sum().groupby('date')['time'].idxmax().str[1]
    cmap = ListedColormap(colorpalette)

    plt.axis = calplot.calplot(series.apply(lambda x: d.get(x,26)),cmap=cmap,edgecolor="#000000",dropzero=True)
    plt.show()

def calplotTotalMinutes():
    series = df.groupby(pd.Grouper(key='date',freq='D')).sum().squeeze()
    plt.axis = calplot.calplot(series)
    plt.show()

def calplotTotalCounts():
    series = df.groupby(pd.Grouper(key='date',freq='D')).count().get("time").squeeze()
    plt.axis = calplot.calplot(series)
    plt.show()

def calplotArtistMinutes(artist):
    series = df[df["artist"]==artist].groupby(pd.Grouper(key='date',freq='D')).sum().squeeze()
    plt.axis = calplot.calplot(series)
    plt.show()
