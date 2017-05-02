from discord.ext import commands
import discord, asyncio
from cogs.utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

class Admin:
    """Commands meant to make changes to the bot or the server."""

    def __init__(self, bot):
        self.bot = bot
        self.permissions_file = 'admins.json'
        self.blacklist_file = 'blacklist.json'
        if not os.path.isfile(self.permissions_file):
            with open (self.permissions_file, 'w') as f:
                f.write('{}')

    @commands.command(pass_context=True, hidden=True, no_pm=True)
    @checks.is_admin()
    async def changenickname(self, ctx, target : str):
        if len(target) > 32:
            await self.bot.change_nickname("That name is too long.")
        elif target == 'none':
            await self.bot.change_nickname(ctx.message.server.me, None)
            await self.bot.say("Nickname removed.")
        else:
            await self.bot.change_nickname(ctx.message.server.me, target)
            await self.bot.say("Nickname changed.")

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def changepresence(self, ctx):
        await self.bot.change_presence(game=discord.Game(name = ctx.message.content.split(' ', 1)[1]))

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def nopresence(self):
        await self.bot.change_presence(game=None)

    @commands.group(pass_context=True, no_pm=True)
    async def permissions(self, ctx):
        '''Shows the list of members that have admin permissions

        Can be used by anyone.

        Append an 'add' or 'remove' after the command to make changes.
        Example: permissions add @Rasmus#1245'''
        permissions_list = []
        server = ctx.message.server
        if ctx.invoked_subcommand is None:
            with open (self.permissions_file) as f:
                admins = json.load(f)
                if server.id not in admins.keys():
                    admins[server.id] = []
                for member_id in admins[server.id]:
                    member = server.get_member(member_id)
                    if member is not None:
                        permissions_list.append(member.name)
            if not permissions_list:
                await self.bot.say("No one has permissions.")
            else:
                await self.bot.say("The following users are in the permissions list: "+', '.join(permissions_list))

    @permissions.command(name='add', pass_context=True, no_pm=True)
    @checks.is_admin()
    async def _add(self, ctx, target : str):
        '''Allows a member to use administrative rights

        Can only be used by the bot owner or the server owner.
        Example: permissions add @Rasmus#1245'''
        if "<@" not in target:
            await self.bot.say("Please use a mention: `addpermission @Rasmus#1245`")
            return
        server = ctx.message.server
        target_id = target[2:-1]
        target_id = target_id.strip('!') #Nicknamed people have a ! next to their id.
        with open (self.permissions_file, 'r') as f:
            admins = json.load(f)
            if str(server.id) not in admins.keys():
                admins[str(server.id)] = []
            if target_id not in admins[str(server.id)]:
                admins[server.id].append(target_id)
                await self.bot.say(target+" has been added to the permissions list.")
            else:
                await self.bot.say(target+" already is in the permissions list.")
        with open (self.permissions_file, 'w') as f:
            json.dump(admins,f,sort_keys = True,indent = 4)

    @permissions.command(name="remove", pass_context=True, no_pm=True)
    @checks.is_admin()
    async def _remove(self, ctx, target : str):
        '''Disallows a member to use administrative rights

        Can only be used by the bot owner or the server owner.
        Example: permissions remove @Rasmus#1245'''
        if "<@" not in target:
            await self.bot.say("Please use a mention: `removepermission @Rasmus#1245`")
            return
        server = ctx.message.server
        target_id = target[2:-1]
        target_id = target_id.strip('!')
        with open (self.permissions_file, 'r') as f:
            admins = json.load(f)
            if str(server.id) not in admins.keys():
                admins[str(server.id)] = []
            if target_id in admins[str(server.id)]:
                admins[server.id].remove(target_id)
                await self.bot.say(target+" has been removed from the permissions list.")
            else:
                await self.bot.say(target+" is not in the permissions list.")
        with open (self.permissions_file, 'w') as f:
            json.dump(admins,f,sort_keys = True,indent = 4)

    @commands.group(pass_context=True, no_pm=True)
    async def blacklist(self, ctx):
        '''Shows the list of members that are blacklisted

        Can be used by anyone.

        Append an 'add' or 'remove' after the command to make changes.
        Example: blacklist add @Rasmus#1245'''
        blacklist_list = []
        server = ctx.message.server
        if ctx.invoked_subcommand is None:
            with open (self.blacklist_file) as f:
                blacklist = json.load(f)
                if str(server.id) not in blacklist.keys():
                    blacklist[str(server.id)] = []
                for member_id in blacklist[str(server.id)]:
                    member = server.get_member(member_id)
                    if member is not None:
                        blacklist_list.append(member.name)
            if not blacklist_list:
                await self.bot.say("No one is blacklisted.")
            else:
                await self.bot.say("The following users are in the blacklist: "+', '.join(blacklist_list))

    @blacklist.command(name='add', pass_context=True, no_pm=True)
    @checks.is_permissive()
    async def _add(self, ctx, target : str):
        '''Disables a person from using my commands.

        Can used by anyone with administrative rights.
        Example: blacklist add @Rasmus#1245'''
        if "<@" not in target:
            await self.bot.say("Please use a mention: `addblacklist @Rasmus#1245`")
            return
        server = ctx.message.server
        target_id = target[2:-1]
        target_id = target_id.strip('!')
        if target_id == "77145785250095104" or target_id == server.owner.id:
            await self.bot.say("You can't blacklist my owner or the server owner.")
            return
        with open (self.blacklist_file, 'r') as f:
            blacklist = json.load(f)
            if str(server.id) not in blacklist.keys():
                blacklist[str(server.id)] = []
            if target_id not in blacklist[str(server.id)]:
                blacklist[server.id].append(target_id)
                await self.bot.say(target+" has been added to the blacklist.")
            else:
                await self.bot.say(target+" is already in the blacklist.")
        with open (self.blacklist_file, 'w') as f:
            json.dump(blacklist,f,sort_keys = True,indent = 4)

    @blacklist.command(name='remove', pass_context=True, no_pm=True)
    @checks.is_permissive()
    async def _remove(self, ctx, target : str):
        '''Enables a person to use my commands.

        Can used by anyone with administrative rights.
        Example: blacklist add @Rasmus#1245'''
        if "<@" not in target:
            await self.bot.say("Please use a mention: `removeblacklist @Rasmus#1245`")
            return
        server = ctx.message.server
        target_id = target[2:-1]
        target_id = target_id.strip('!')
        with open (self.blacklist_file, 'r') as f:
            blacklist = json.load(f)
            if str(server.id) not in blacklist.keys():
                blacklist[str(server.id)] = []
            if target_id in blacklist[str(server.id)]:
                blacklist[server.id].remove(target_id)
                await self.bot.say(target+" has been removed from the blacklist.")
            else:
                await self.bot.say(target+" is not in the blacklist.")
        with open (self.blacklist_file, 'w') as f:
            json.dump(blacklist,f,sort_keys = True,indent = 4)

    def is_pink(self, message):
        return message.author == self.bot.user

    @commands.command(pass_context=True,no_pm=True)
    @checks.is_permissive()
    async def pinkdelete(self, ctx):
        '''Used to delete my own messages

        pinkdelete <count>
        Example: pinkdelete 10
        It also counts messages that aren't sent by me, which you should take into account.
        '''
        message = ctx.message
        if ' ' in message.content:
            purge_limit = message.content.split(' ',1)[1]
            if int(purge_limit) > 100:
                await self.bot.say("Can't delete more than 100.")
                return
        else:
            await self.bot.say('Please specify the count `pinkdelete <1-100>`. Keep in mind that it also counts messages that aren\'t sent by me')
        deleted = await self.bot.purge_from(message.channel, limit=int(purge_limit), check=self.is_pink)
        await self.bot.say('Deleted {} message(s)'.format(len(deleted)))

        @commands.command(pass_context=True, hidden=True)
        @checks.is_owner()
        async def say(self, ctx):
            await self.bot.say(ctx.message.content)

def setup(bot):
    bot.add_cog(Admin(bot))
