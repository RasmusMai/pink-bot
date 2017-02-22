from discord.ext import commands
import discord, asyncio
from .utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Rofoc:
    '''Rofoc specific commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['colour'], pass_context=True)
    async def color(self,ctx):
        '''Change the color of your own name.
        Example: color green'''
        message = ctx.message
        possible_colors = ['red','blue','green','purple','orange','yellow','grey','brown','none']
        requested_color = message.content.split(' ', 1)[1]
        requested_color = requested_color.lower().strip()
        if requested_color in possible_colors:
            for server_role in message.server.roles:
                if server_role.name.lower() == requested_color:
                    role_given = server_role
            for color in possible_colors:
                for current_role in message.author.roles:
                    if current_role.name.lower() in possible_colors:
                        if requested_color == current_role.name.lower():
                            await self.bot.say("You already have that color")
                            return
                        await self.bot.remove_roles(message.author, current_role)
            if requested_color == 'none':
                await self.bot.say("You are now without a color. Doesn\'t it feel great to be different!")
            else:
                await self.bot.add_roles(message.author, role_given)
                await self.bot.say("Your color is now "+ requested_color)
        else:
            await self.bot.say("I can only give you one of the following colors: red, blue, green, purple, orange, yellow, grey and brown.")


def setup(bot):
    bot.add_cog(Rofoc(bot))
