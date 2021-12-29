import os, json, datetime, re
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import july

datafiles = list(filter(lambda x: re.search('StreamingHistory[0-9]*\.json',x),os.listdir()))

numprint = 10


artists = dict()
songs = dict()

topartistday = dict()
counttopartistday = dict()

topsongday = dict()
counttopsongday = dict()

topartistdayTime = dict()
timetopartistday = dict()

topsongdayTime = dict()
timetopsongday = dict()

dayArtists = dict()
daySongs = dict()

for datafile in datafiles:
    with open(datafile,'r',encoding="utf-8") as file:
        data = json.load(file)
        for song in data:
            artist = song['artistName']
            trackname = song['trackName']
            date = datetime.datetime.strptime(song['endTime'],'%Y-%m-%d %H:%M')
            day = str(date.date())
            time = int(song['msPlayed'])/60000.0
            
            # artist
            artists.setdefault(artist,[0,0])
            artists[artist][0] += 1
            artists[artist][1] += time
            
            # song
            songs.setdefault(trackname,[0,0])
            songs[trackname][0] += 1
            songs[trackname][1] += time

            # daily artists
            dayArtists.setdefault(day,dict())
            dayArtists[day].setdefault(artist,[0,0])
            dayArtists[day][artist][0] += 1
            dayArtists[day][artist][1] += time
            
            # daily songs
            daySongs.setdefault(day,dict())
            daySongs[day].setdefault(trackname,[0,0])
            daySongs[day][trackname][0] += 1
            daySongs[day][trackname][1] += time
            
# artist day count
for day in dayArtists:
    topartistday[day] = sorted(dayArtists[day].items(),key=lambda x: -x[1][0])[0]

for artist in topartistday.values():
    counttopartistday[artist[0]] = counttopartistday.get(artist[0],0)+1
    
# artist day time
for day in dayArtists:
    topartistdayTime[day] = sorted(dayArtists[day].items(),key=lambda x: -x[1][1])[0]

for artist in topartistdayTime.values():
    timetopartistday[artist[0]] = timetopartistday.get(artist[0],0)+1

# song day count
for day in daySongs:
    topsongday[day] = sorted(daySongs[day].items(),key=lambda x: -x[1][0])[0]

for song in topsongday.values():
    counttopsongday[song[0]] = counttopsongday.get(song[0],0)+1
    
# song day time
for day in daySongs:
    topsongdayTime[day] = sorted(daySongs[day].items(),key=lambda x: -x[1][1])[0]

for song in topsongdayTime.values():
    timetopsongday[song[0]] = timetopsongday.get(song[0],0)+1

counttopartistday = sorted(list(counttopartistday.items()),key=lambda x: -x[1])
counttopsongday = sorted(list(counttopsongday.items()),key=lambda x: -x[1])

timetopartistday = sorted(list(timetopartistday.items()),key=lambda x: -x[1])
timetopsongday = sorted(list(timetopsongday.items()),key=lambda x: -x[1])


print("Most listened artists (minutes):\n")
print(*sorted(list(artists.items()),key=lambda x: -x[1][1])[0:numprint],sep="\n")

print()
print("Most listened artists (count):\n")
print(*sorted(list(artists.items()),key=lambda x: -x[1][0])[0:numprint],sep="\n")

print()
print("Most listened songs (minutes):\n")
print(*sorted(list(songs.items()),key=lambda x: -x[1][1])[0:numprint],sep="\n")

print()
print("Most listened songs (count):\n")
print(*sorted(list(songs.items()),key=lambda x: -x[1][0])[0:numprint],sep="\n")

print()
print("Days artist has been the most listened to (count):\n")
print(*counttopartistday[0:numprint],sep="\n")

print()
print("Days song has been the most listened to (count):\n")
print(*counttopsongday[0:numprint],sep="\n")

print()
print("Days artist has been the most listened to (time):\n")
print(*timetopartistday[0:numprint],sep="\n")

print()
print("Days song has been the most listened to (time):\n")
print(*timetopsongday[0:numprint],sep="\n")


colorpalette = ['#2f4f4f','#8b4513','#808000','#008000','#000080','#9acd32',
'#8fbc8f','#8b008b','#ff0000','#ff8c00','#ffd700','#6a5acd','#7fff00','#9400d3',
'#00fa9a','#dc143c','#00ffff','#00bfff','#0000ff','#d8bfd8','#db7093','#f0e68c',
'#ff1493','#ffa07a','#ee82ee'] + ['#ffffff']*350

mindate, maxdate = min(dayArtists), max(dayArtists)

def plotHeatMap(freqDailyTop: list, dailyTop: dict, title=None):
    top = {a[0]:i+1 for i,a in enumerate(freqDailyTop)}

    dates = july.utils.date_range(mindate,maxdate)
    data = [top.get(dailyTop.get(str(day),[0,0])[0]) for day in dates]
    ax = july.heatmap(dates,data,cmap=ListedColormap(colorpalette[:len(top)]), month_grid=True)

    sortedtop = [x[0] for x in sorted(list(top.items()),key=lambda x: x[1])]

    # legend
    for i,name in enumerate(sortedtop):
        if i >= 25:
            break
        ax.plot(0,0,label=str(i+1)+". "+name,marker="s",markersize=8,linewidth=0,color=colorpalette[i])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size': 6})
    ax.plot(0,0,marker="s",markersize=8,linewidth=0,color='#ffffff')

    plt.axes = ax
    plt.title(title)
    plt.show()

plotHeatMap(counttopartistday, topartistday, "Daily Top Artist (by count)")
plotHeatMap(timetopartistday, topartistdayTime, "Daily Top Artist (by time)")
plotHeatMap(counttopsongday, topsongday, "Daily Top Song (by count)")
plotHeatMap(timetopsongday, topsongdayTime, "Daily Top Song (by time)")
