# Pink
A discord bot born from severe autism using Python 3.5. Should run correctly on both Windows and Linux, I have yet to test it on a Mac.

Uses the Discord API from https://github.com/Rapptz/discord.py

In addition, it utilizes https://github.com/praw-dev/praw for Reddit and https://github.com/jsvine/markovify for generating Markov chains. `pip3 install -r requirements.txt` could simply be used for installation of dependencies.

The credentials.json used for authentication should look something like.
```
{
  "token": "discord bot token",
  "reddit_secret": "reddit app secret",
  "reddit_id": "reddit app id",
  "openweathermap": "openweathermap api key"
}
```
