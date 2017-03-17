from discord.ext import commands
import discord, asyncio
from cogs.utils import checks
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json

initial_cogs = [
    'cogs.general',
    'cogs.vanity',
    'cogs.stats',
    'cogs.reddit',
    'cogs.rofoc',
    'cogs.audio',
    'cogs.admin'
]

description = '''Hey, I'm Pink.
Born from severe crippling depression in addition to autism.

'''
prefix = ""
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=True)

@bot.event
async def on_ready():
    print('Logged in, my nickname is: ' + bot.user.name)
    print('My id is: ' + bot.user.id)
    print('The time: ' + str(datetime.datetime.now()))
    print('<><><><><><><><><><><><><><><><><><><><><><><><><>')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    with open (blacklist_file, 'r') as f:
        blacklist = json.load(f)
        if str(message.server.id) not in blacklist.keys():
            blacklist[str(message.server.id)] = []
        if message.author.id in blacklist[str(message.server.id)]:
            return
    if message.content.lower().strip(' ') == ("ayy"):
        await bot.send_message(message.channel,"lmao")
    if message.content.startswith(prefix):
        await bot.process_commands(message)
    else:
        if "weeb" in message.content.lower() or "weebs" in message.content.lower() or "weeaboo" in message.content.lower() or "weeaboos" in message.content.lower():
            weeb_file = "weeb.txt"
            with open(weeb_file) as file:
                weebarray = []
                for item in os.listdir("weeb_pics"):
                    weebarray.append(item)
                for value in file.read().split('🐢'):
                    weebarray.append(value)
                msg_to_be_sent = random.choice(weebarray)
            if re.match('([^\s]+(\.(?i)(jpg|png|gif|bmp))$)', msg_to_be_sent):
                await bot.send_file(message.channel, 'weeb_pics/'+msg_to_be_sent)
            else:
                await bot.send_message(message.channel,msg_to_be_sent)

@bot.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    if isinstance(error, commands.CheckFailure):
        if "nsfw" in ctx.message.content.lower():
            await bot.send_message(channel, "I won't send NSFW messages in non-NSFW channels, sorry.")
        else:
            await bot.send_message(channel, "You're not allowed to do that, sorry.")
    elif isinstance(error, commands.CommandNotFound):
            pass
    elif isinstance(error, commands.DisabledCommand):
            await bot.send_message(channel, "That command is disabled.")
    return bot

@bot.event
async def on_member_join(member):
	await bot.send_message(member.server, member.mention + " has joined.")
@bot.event
async def on_member_remove(member):
	await bot.send_message(member.server, member.mention + " has left :o")

@bot.command(pass_context=True, hidden=True)
@checks.is_owner()
async def shutdown(ctx):
    await bot.say("Bye!")
    await bot.logout()

def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)

if __name__ == '__main__':
    credentials = load_credentials()
    if 'token' not in credentials.keys():
        print("No token provided. Exiting.")
        exit()
    for extension in initial_cogs:
        try:
            if extension == 'cogs.reddit' and 'reddit_secret' not in credentials.keys():
                print ('Ignoring '+extension+'. No key in credentials.json provided.')
            else:
                print('Loading extension -- ' + extension, end='')
                bot.load_extension(extension)
                print(' -- Success')
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    try:
        os.system('clear')
    except:
        os.system('cls')
    blacklist_file = 'blacklist.json'
    print('<><><><><><><><><><><><><><><><><><><><><><><><><>')
    token = credentials['token']
    bot.run(token)
