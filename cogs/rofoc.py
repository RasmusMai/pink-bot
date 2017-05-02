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
    async def color(self, ctx, requested_color : str):
        '''Change the color of your own name.
        Example: color green'''
        message = ctx.message
        if requested_color.startswith('#'):
            await self.do_hex_color(requested_color, ctx.message)
            return
        possible_colors = ['red','blue','green','purple','orange','yellow','grey','brown','none']
        requested_color = requested_color.lower().strip()
        if requested_color in possible_colors:
            for server_role in message.server.roles:
                if server_role.name.lower() == requested_color:
                    role_given = server_role
            for color in possible_colors:
                for current_role in message.author.roles:
                    if current_role.name.lower() in possible_colors or current_role.name.startswith('#'):
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
            await self.bot.say("I can only give you one of the following colors: red, blue, green, purple, orange, yellow, grey and brown. You can also use hex codes like: `color ##A7A502`")

    async def do_hex_color(self, requested_color, message):
        possible_colors = ['red','blue','green','purple','orange','yellow','grey','brown','none']
        requested_color = requested_color.lower()
        if len(requested_color) > 7:
            await self.bot.say("That's not a proper hex code. Example `#F02BA2`")
            return
        try:
            int(requested_color[1:],16)
        except:
            await self.bot.say("That's not a proper hex code. They can only contain numbers from 0-9 and letters from A-F")
            return
        for current_role in message.author.roles:
            if current_role.name.lower() in possible_colors or current_role.name.startswith('#'):
                if requested_color == current_role.name.lower():
                    await self.bot.say("You already have that color")
                    return
                await self.bot.remove_roles(message.author, current_role)
        for server_role in message.server.roles:
            if server_role.name.lower() == requested_color:
                role_given = server_role
                await self.bot.add_roles(message.author, role_given)
                await self.bot.say("Your color is now "+ requested_color)
                return
        await self.bot.create_role(message.server, name=requested_color, colour=discord.Colour(int(requested_color[1:],16)), hoist=False)
        await asyncio.sleep(0.6)
        for server_role in message.server.roles:
            if server_role.name.lower() == requested_color:
                role_given = server_role
        await self.bot.add_roles(message.author, role_given)
        await self.bot.say("Your color is now "+ requested_color)
        return


def setup(bot):
    bot.add_cog(Rofoc(bot))
