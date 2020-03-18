import tweepy
import time
import random
from keys import *
import genius_lyric as gl


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
LAST_SEEN_ID = 'txt/last_seen_id.txt'
LAST_SEEN_USER = 'txt/last_seen_user.txt'
LYRIC_REPLY_COUNT = 'txt/lyric_reply_count.txt'
ARTIST_AND_SONG = 'txt/artist_and_song.txt'
MENTION_LYRIC = 'txt/mention_lyric.txt'
TWIT_LYRIC = 'txt/twit_lyric.txt'

#takes a mention and a text reply string as arguments
#example of mention: mention = mentions[0]
def reply_to_tweet(mention, reply):
    reply_screen_name = mention._json['user']['screen_name']
    api.update_status(status='@' + reply_screen_name + ' '+ reply, in_reply_to_status_id = mention.id, in_reply_to_status_id_str = str(mention.id))

def retrieve_last_seen_id(file_name):
    try:
        f_read = open(file_name, 'r')
        last_seen_id = int(f_read.read().strip())
        f_read.close()
        return last_seen_id
    except ValueError:
        return 0

def store_last_seen_id(file_name, last_seen_id):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def retrieve_last_seen_user(file_name):
    try:
        f_read = open(file_name, 'r')
        last_seen_user = f_read.read().strip()
        f_read.close()
        return last_seen_user
    except ValueError:
        return 0

def store_last_seen_user(file_name, last_seen_user):
    f_write = open(file_name, 'w')
    f_write.write(last_seen_user)
    f_write.close()
    return

def retrieve_lyric_reply_count(file_name):
    try:
        f_read = open(file_name, 'r')
        last_seen_user = int(f_read.read().strip())
        f_read.close()
        return last_seen_user
    except ValueError:
        return 0

def store_lyric_reply_count(file_name, lyric_reply_count):
    f_write = open(file_name, 'w')
    f_write.write(str(lyric_reply_count))
    f_write.close()
    return

def retrieve_artist_and_song(file_name):
    try:
        f_read = open(file_name, 'r')
        a_s = f_read.read().strip()
        f_read.close()
        artist = a_s[a_s.find("artist:") + 7:a_s.find("song:")].strip()
        song = a_s[a_s.find("song:") + 5:].strip()
        artist_and_song = {
            "artist": artist,
            "song": song
        }
        return artist_and_song
    except ValueError:
        return 0

# Reads from the session and stores it in an array
def retrieve_twit_lyric(file_name):
    try:
        f_read = open(file_name, 'r')
        twit_lyric = f_read.read().strip()
        f_read.close()
        tw = twit_lyric.splitlines()
        for i in range(len(tw)):
            tw[i] = tw[i].strip()
        return tw
    except ValueError:
        return 0
# Takes in a filename and a list from gl.makeLyricParts("t", part) 
# Writes to the file once a session when user picks a song
def store_twit_lyric(file_name, twit_lyric):
    f_write = open(file_name, 'a')
    for i in range(len(twit_lyric)):
        f_write.write(" " + twit_lyric[i] + "\n")
    f_write.close()
    return

def retrieve_mention_lyric(file_name):
    try:
        f_read = open(file_name, 'r')
        mention_lyric = f_read.read().strip()
        f_read.close()
        return mention_lyric
    except ValueError:
        return 0

def store_mention_lyric(file_name, mention_lyric):
    f_write = open(file_name, 'a')
    f_write.write(" " + mention_lyric.lower() + " ")
    f_write.close()
    return


# Cleans up user tweet to return dict of song and artist input str must be eg."artist: katy perry song: roar" format
# also stores the artist and song in a txt file
def get_artist_and_song(replystr):
    replystr = replystr.lower()
    if "artist:" and "song:" in replystr:
        replystr = replystr.strip()
        artist = replystr[replystr.find("artist:") + 7:replystr.find("song:")].strip()
        song = replystr[replystr.find("song:") + 5:].strip()
        artist_and_song = {
            "artist": artist,
            "song": song
        }

        f_write = open(ARTIST_AND_SONG, 'w')
        f_write.write("artist: " + artist + " song: " + song)
        f_write.close()
        return artist_and_song
    else:
        return 0

# Completely clears all the temporary txt files. Use after the user thread/session ends
def clearThread():
    open(LAST_SEEN_USER, 'w').close()
    open(LYRIC_REPLY_COUNT, 'w').close()
    open(ARTIST_AND_SONG, 'w').close()
    open(MENTION_LYRIC, 'w').close()
    open(TWIT_LYRIC, 'w').close()
    print("Txt files cleared")
    return 

#list of words for testing purposes
emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😊", "😇", "🙂", "😉", "😌", "😍", "😘", "😗", "😙", "😚", "😋", "😛", "😝", "😜", "🤓", "😎", "🤩", "😏", "🤗", "🤑", "🤠"]
greetings = ["Hi", "Hey there", "Hello", "Hello there", "Hey"]



def reply_to_mentions():
    print("Retrieving and replying to tweets...")

    if api.mentions_timeline() == []:
        print("No mentions to respond to")
        #resets the last seen id file with an empty string, if there are no mentions
        f_write = open(LAST_SEEN_ID, 'w')
        f_write.write("")
        f_write.close()
    else:
        #check if text file is empty, if it is, mentions sorts through every mention
        if retrieve_last_seen_id(LAST_SEEN_ID) == 0:
            mentions = api.mentions_timeline()
        else:
            last_seen_id = retrieve_last_seen_id(LAST_SEEN_ID)
            mentions = api.mentions_timeline(since_id = last_seen_id)
        ## make the music part here

        # reversed to show the oldest tweet first and newest tweet last
        # use 1208618631946358785 aka tweet 1 id for testing
        for mention in reversed(mentions):
            print(str(mention.id) + ' - ' + mention.text)
            store_last_seen_id(LAST_SEEN_ID, mention.id)

            reply_screen_name = mention._json['user']['screen_name']
            name = mention._json['user']['name']
            ## start thread from beginning if the usernames havent been seen (first 2 options)
            if retrieve_last_seen_user(LAST_SEEN_USER) == 0:
                store_last_seen_user(LAST_SEEN_USER, reply_screen_name)
                reply = random.choice(greetings) + " " + name + "! " + random.choice(emojis) + " Tell me an artist and a song! " + random.choice(emojis) + "🎤" + " In this format ➡️ artist: artistname song: songname"
            elif reply_screen_name != retrieve_last_seen_user(LAST_SEEN_USER):
                store_last_seen_user(LAST_SEEN_USER, reply_screen_name)
                reply = random.choice(greetings) + " " + name + "! " + random.choice(emojis) + " Tell me an artist and a song! " + random.choice(emojis) + "🎤" + " In this format ➡️ artist: artistname song: songname"
            ## continue thread here
            elif reply_screen_name == retrieve_last_seen_user(LAST_SEEN_USER):
                ## continue thread until finished then clear 
                ## use clearThread() to remove all temp file info

                # If the format of the tweet is valid eg. artist: artistname song: songname
                try:
                    if get_artist_and_song(mention.text) != 0 and retrieve_lyric_reply_count(LYRIC_REPLY_COUNT) == 0:
                        part = gl.makePart(get_artist_and_song(mention.text)["artist"], get_artist_and_song(mention.text)["song"])
                        twit = gl.makeLyricParts("t", part)
                        store_twit_lyric(TWIT_LYRIC, twit)
                        # error handling for when the song can't be found on genius
                        try:
                            reply = twit[0]
                            store_lyric_reply_count(LYRIC_REPLY_COUNT, 1)
                            print("It's a match")
                        except:
                            print("Cannot find song")
                            reply = "Sorry our kittenBOTS™️ don't recognize that song, try again!"
                            reply_to_tweet(mention, reply)
                            print("replied with: " + reply)
                            clearThread()
                            ## Deletes most recent status then tries again
                            api.destroy_status(api.user_timeline()[0].id)
                            reply_to_mentions()

                    # Lyric session goes on until the length of the twit lyrics
                    elif retrieve_lyric_reply_count(LYRIC_REPLY_COUNT) < len(retrieve_twit_lyric(TWIT_LYRIC)):
                        tw = retrieve_twit_lyric(TWIT_LYRIC)
                        # Storing the user's reply in mention_lyric as a single string in mention_lyric.txt file
                        store_mention_lyric(MENTION_LYRIC, mention.text)
                        reply = tw[retrieve_lyric_reply_count(LYRIC_REPLY_COUNT)]
                        store_lyric_reply_count(LYRIC_REPLY_COUNT, retrieve_lyric_reply_count(LYRIC_REPLY_COUNT) + 1)

                    # When it gets to the last reply, game is over and final tweet is sent and game is reset
                    elif retrieve_lyric_reply_count(LYRIC_REPLY_COUNT) == len(retrieve_twit_lyric(TWIT_LYRIC)):
                        part = gl.makePart(retrieve_artist_and_song(ARTIST_AND_SONG)["artist"], retrieve_artist_and_song(ARTIST_AND_SONG)["song"])
                        u_part = gl.makeLyricParts("u", part)
                        my_part = retrieve_mention_lyric(MENTION_LYRIC)
                        acc = gl.getAccuraccy(u_part, my_part)
                        ## These comments are a little extra tbh
                        # if acc > 80:
                        #     extra = " You're skills are impeccable! Are you sure you're not a bot yourself 🤔"
                        # elif acc > 50:
                        #     extra = " Not bad for a rookie 😉"
                        # else:
                        #     extra = " Better luck next time? 🤷‍♀️"
                        reply = "Thanks for singing with me, " + mention._json['user']['name'] + "! " + random.choice(emojis) + " According to our highly trained lyric analyst kittenBOTS™️, your lyrics were " + str(acc) + "%" + " accturate!"
                        clearThread()
                except:
                    print("Invalid reply format")
                    reply = "Wrong format must be ➡️ artist: artistname song: songname"
                    reply_to_tweet(mention, reply)
                    print("replied with: " + reply)
                    clearThread()
                    ## Deletes most recent status then tries again
                    api.destroy_status(api.user_timeline()[0].id)
                    reply_to_mentions()


            #storing the reply in its own string variable
            reply_to_tweet(mention, reply)
            print("replied with: " + reply)


while True:
        reply_to_mentions()
        time.sleep(15)













