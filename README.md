# Sing To Me Bot: A Twitter bot that sings song lyrics with you! 🎤
A Twitter bot built in Python - created by [@milnorms](https://github.com/milnorms).
Inspired by: [@ykdojo's twitter sample bot](https://github.com/ykdojo/twitterbotsample).

Uses the [tweepy](http://docs.tweepy.org/en/latest/) and [lyricsgenius](https://github.com/johnwmillr/LyricsGenius) libraries.

---

## Set up notes

### How to install Tweepy

First, check your Python version with ``python3 --version`` or ``python --version`` on console (terminal/shell/command prompt).

#### If you don't have Python 3 installed (if the above command fails):

Either install Python 3 on your computer OR use something like PythonAnywhere (https://csdojo.io/py).

#### If you have Python 3.6, you can just run:

``pip3 install tweepy``

#### If you have Python 3.7, run the following instead:

``pip3 install -U git+https://github.com/tweepy/tweepy.git@2efe385fc69385b57733f747ee62e6be12a1338b``

If the above command doesn't work, try replacing ``pip3`` with ``pip`` also.

#### How to install lyricsgenius

``pip install lyricsgenius``

---

## How to use Sing To Me Bot

![Sample of singtomebot thread](https://media.giphy.com/media/UX5tDnO1pNYTClyjKO/giphy.gif)

1. Tweet [@singtomebot](https://twitter.com/singtomebot) an initial tweet
2. Follow [@singtomebot](https://twitter.com/singtomebot)'s reply asking for an artist name and song name (must be in the right order or else the bot resets and the thread ends)
3. [@singtomebot](https://twitter.com/singtomebot) will reply with the first line of the chorus of your chosen song
4. User replies back to that tweet with the next line of the chorus
5. [@singtomebot](https://twitter.com/singtomebot) replies with the next line of the chorus
6. Continue until the chorus is finishes
7. [@singtomebot](https://twitter.com/singtomebot) rates how accurate your lyrics were to the original song lyrics and thread ends!

---

## Files
- **twit.py** - This is the main file that includes all the logic and runs the main twitter related functionality. Imports functions from lyric_genius.py to handle everything to do with lyrics
- **last_seen_id.txt** - This will contain the ID of the tweet that twit.py has seen last. If you see any errors when running the main file, try replacing the content with the ID of one of the tweets you want to examine.
- **keys_format.py** - This file is not meant to be used directly. Instead, copy this file in the same folder and rename it to keys.py. Then, put your Twitter API keys in keys.py. That way, my_twitter_bot.py will be able to use this information.
- **genius_keys_format.py** - This file is not meant to be used directly. Instead, copy this file in the same folder and rename it to genius_keys.py. Then, put your Genius lyrics API keys in genius_keys.py.
- **last_seen_user.txt** - This contains the last seen username that twit.py has seen. If the username hasn't been seen, the bot starts a new thread, if it has been seen, the bot continues the thread.
- **lyric_reply_count.txt** - This keeps a record of the amount of replies twit.py has seen. If there are no replies or the text file is empty, the bot starts the thread from the beginning.
- **artist_and_song.txt** - This keeps a record of the artist and song the user chose. twit.py retrieves the data from the txt file and uses it to make requests to the lyrics genius api.
- **mention_lyric.txt** - This stores the text content of the tweets from the user during the lyric part of the thread. twit.py then retrieves the data from this file at the end of the thread to analyze how accurate the user's lyrics were.
- **twit_lyric.txt** - This keeps a record of the bot's lyric responses in the thread to keep track of which part of the chorus the bot is replying at.
- **genius_lyric.py** - This provides the main song and lyric functionality.
