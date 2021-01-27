from discord.ext import commands
import os
import sys
import json
import time
import traceback

description = '''
autism.
'''

prefix = ''


bot = commands.Bot(command_prefix=prefix, description=description)

cogs = [
    'cogs.general',
    'cogs.piston',
    'cogs.admin'
]


def _do_checks():
    if not os.path.isfile('credentials.json'):
        print("No 'credentials.json' found. An example is given on the GitHub page.")
        exit()
    if not os.path.exists('markov/'):
        os.makedirs('markov/')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(bot.user.id)
    print('------')


def _load_credentials():
    with open('credentials.json') as f:
        return json.load(f)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    """
    if message.guild:
        with open('markov/'+str(message.guild.id)+'.txt', 'a', encoding="utf8") as markov_file:
            markov_file.write(message.content+'\n')
    """
    if message.content.startswith(prefix):
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    channel = ctx.message.channel
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(channel, "That command is disabled.")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send(ctx.message.author, 'Sorry, I can\'t do this in private messages.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
    return bot


"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("hi"):
        await message.channel.send("i have the gay now")
"""


if __name__ == "__main__":
    _do_checks()
    credentials = _load_credentials()
    for extension in cogs:
        try:
            print('Loading extension -- ' + extension, end='')
            bot.load_extension(extension)
            print(' -- Success')
            time.sleep(0.2)  # No real purpose, it just looks cooler.
        except Exception as e:
            print('\nFailed to load extension {}\n{}: {}\n'.format(extension, type(e).__name__, e))
            time.sleep(1)
    token = credentials['token']
    bot.run(token)
