from discord.ext import commands
import discord, asyncio
from .utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Stats:
    """Statistics"""

    def __init__(bot, self):
        self.bot = bot

def setup(bot):
    bot.add_cog(Stats(bot))
