from discord.ext import commands
import discord, asyncio
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

def is_owner_check(message):
    return message.author.id == '77145785250095104'

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))

def is_nsfw_check(message):
    return "nsfw" in message.channel.name.lower()

def is_nsfw():
    return commands.check(lambda ctx: is_nsfw_check(ctx.message))
