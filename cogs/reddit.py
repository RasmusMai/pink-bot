from discord.ext import commands
import discord, asyncio
from .utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Reddit:
    """Commands related to Reddit, uses the Python library 'praw'."""

    def __init__(self, bot):
        self.bot = bot
        with open('credentials.json') as f:
            credentials = json.load(f)
            self.reddit = praw.Reddit(client_id=credentials['reddit_id'],
                        client_secret=credentials['reddit_secret'],
                        user_agent='pink.py Discord bot by Rasmus')

    @commands.command()
    async def aww(self):
        '''Returns a post from r/aww'''
        await self.bot.say(self.get_subreddit("aww").split(';',1)[1])

    @commands.command(aliases=['neko','kitty'])
    async def cat(self):
        '''Returns a picture of a cat.
        Uses r/meow_irl, r/cats or r/catpictures'''
        await self.bot.say(self.get_subreddit(random.choice(['meow_irl','cats','catpictures'])).split(';',1)[1])

    @commands.command(aliases=['doggo','pupper','doge'])
    async def dog(self):
        '''Returns a picture of a dog.
        Uses r/woof_irl, r/woofbarkwoof or r/dogpictures'''
        await self.bot.say(self.get_subreddit(random.choice(['woof_irl','woofbarkwoof','dogpictures'])).split(';',1)[1])

    @commands.command(pass_context = True)
    async def subreddit(self, ctx):
        '''Returns a random post from the subreddit.
        Completely ignores NSFL posts and NSFW posts require the channel to have the word "nsfw" in their name.
        Example: subreddit funny'''
        message_content = ctx.message.content.lower()
        query_subreddit = message_content.split(' ',1)[1]
        nsfw_channel = False
        subreddit_top = False
        if "nsfw" in ctx.message.channel.name:
            nsfw_channel = True
        if query_subreddit.endswith(' top'):
            query_subreddit = query_subreddit[:-4]
            subreddit_top = True
        redditresponse = self.get_subreddit(query_subreddit,subreddit_top=subreddit_top,nsfw_channel=nsfw_channel)
        if ";" not in redditresponse:
            await self.bot.say(redditresponse)
            return
        await self.bot.say("**"+redditresponse.split(';',1)[0]+"**\n"+redditresponse.split(';',1)[1])

    def get_subreddit(self, subreddit,subreddit_top=False, nsfw_channel=False):
        nsfw_found = False
        if ' ' in subreddit:
            #await self.bot.say("Subreddit names can't contain spaces. Use underscore instead: `meow_irl` and in some cases the words are joined together: `OldLadiesBakingPies`")
            return ("Subreddit names can't contain spaces. Use underscore instead: `meow_irl` and in some cases the words are joined together: `OldLadiesBakingPies`")
        post_array = []
        try:
            if subreddit_top:
                for submission in self.reddit.subreddit(subreddit).top('all'):
                    if "nsfl" not in submission.title.lower() or "nsfw\/l" not in submission.title.lower():
                        if submission.over_18 and not nsfw_channel:
                            nsfw_found = True
                        else:
                            post_array.append(submission.title+";"+submission.url)
            else:
                for submission in self.reddit.subreddit(subreddit).hot(limit=25):
                    if "nsfl" not in submission.title.lower() or "nsfw\/l" not in submission.title.lower():
                        if submission.over_18 and not nsfw_channel:
                            nsfw_found = True
                        else:
                            post_array.append(submission.title+";"+submission.url)
            #await self.bot.say(random.choice(post_array))
            return (random.choice(post_array))
        except IndexError:
            if nsfw_found:
                #await self.bot.say("I couldn't find any sfw posts in that subreddit and I won't send NSFW posts in non-NSFW channels, sorry.")
                return ("I couldn't find any sfw posts in that subreddit and I won't send NSFW posts in non-NSFW channels, sorry.")
            else:
                #await self.bot.say("I didn't find any posts in that subreddit. Right now I can only send images that end with `.jpg`, `.png` or `.gif`, gfycat, imgur links and Youtube videos. Let Rasmus know if you'd also like text posts.")
                return ("I didn't find any posts in that subreddit.")
        except:
            #await bot.say("I couldn't fetch that subreddit. Could be that the subreddit requires user login or it just doesn't exist.")
            return ("I couldn't fetch that subreddit. Could be that the subreddit requires user login or it just doesn't exist.")


def setup(bot):
    bot.add_cog(Reddit(bot))
