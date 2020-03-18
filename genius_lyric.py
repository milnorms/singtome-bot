import lyricsgenius
from genius_keys import *
import difflib as dl

# uses the genius api to fetch lyrics
genius = lyricsgenius.Genius(CLIENT_ACCESS_TOKEN)

# Retrieving artist name. Not necissary to find song lyrics
def getArtistName(artistName):
    artist = genius.search_artist(artistName, max_songs=1, sort="popularity", get_full_info = False)
    return artist.name

# Returns a string of the song lyrics
def getLyrics(artistName, songTitle):
    song = genius.search_song(songTitle, artistName)
    if song:
        return song.lyrics
    else:
        song = genius.search_song(artistName, songTitle)
        return song.lyrics

# Splices different parts of the lyrics into small section (chorus)
# Returns lyric part and cleans them up in a list
def makePart(a, s):
    lyrics = getLyrics(a, s).lower()
    lyrics = lyrics.replace(":", "")
    lyrics = lyrics.replace("[", "")
    lyrics = lyrics.replace("]", "")
    l_list = lyrics.splitlines()

    c_element = 0
    v_element = 0
    found = False
    chorus = ""
    for i in range(len(l_list)):
        if "chorus" in l_list[i] and "pre-chorus" not in l_list[i]:
            c_element = i
            found = True

        if "verse" in l_list[i] and i > c_element:
            v_element = i

            if found:
                break

    i = c_element + 1
    while i < v_element:
        chorus += l_list[i]  + "\n"
        i += 1

    partList = chorus.splitlines()
    part = []
    for i in range(len(partList)):
        if len(partList[i]) != 0:
            part.append(partList[i])
    return part

# Input either "t" or "u" to obtain list of lyrics parts. userPart either "t" for twitbot or "u" for user
def makeLyricParts(userPart, part):
    # Loops through every other line and adds it to twitlyrics
    if userPart == "t":
        twitsLyrics = []
        for i in range(0, len(part), 2):
            twitsLyrics.append(part[i])
        return twitsLyrics
    if userPart == "u":
        userLyrics = []
        for i in range(1, len(part), 2):
            userLyrics.append(part[i])
        return userLyrics

# Takes in a u_part which is makeLyricParts("u", part) / a list of the real lyrics that the user is supposed to match and
# my_part which is the user input lyrics MUST BE A STRING. Returns a str of the percentage of accuracy
def getAccuraccy(u_part, my_part):
    u_part_str = ""

    for i in range(len(u_part)):
        u_part_str += u_part[i] + " "

    s = dl.SequenceMatcher(lambda x: x==",", my_part, u_part_str)
    return round(s.real_quick_ratio() * 100, 1)
     
# uncomment for example on how to make the twitterbot part and the users part
# part = makePart("ariana grande", "7 rings")
# t_part = makeLyricParts("t", part)
# u_part = makeLyricParts("u", part)


# my_part = "i want  i want it i got one, if i see it, i like it, i want it, i got it"
# print(getAccuraccy(u_part, my_part))



    

















