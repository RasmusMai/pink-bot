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

def is_admin_check(message):
    return message.author.id == '77145785250095104' or message.author == message.server.owner

def is_admin():
    return commands.check(lambda ctx: is_admin_check(ctx.message))

def is_permissive_check(message):
    with open ("admins.json") as f:
        admins = json.load(f)
        print (admins[str(message.server.id)])
        if str(message.author.id) in admins[str(message.server.id)] or message.author == message.server.owner:
            return True
        else:
            return False
def is_permissive():
    return commands.check(lambda ctx:is_permissive_check(ctx.message))
