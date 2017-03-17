from discord.ext import commands
import discord, asyncio
from cogs.utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Audio:

    def __init__(self, bot):
        self.bot = bot
        if discord.opus.is_loaded():
            print ("Opus loaded")
        else:
            print ("Opus not loaded")

def setup(bot):
    bot.add_cog(Audio(bot))
