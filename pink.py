import discord
from discord.ext import commands
import random

description = '''Pink - Your general purpose Discord friend.
I'm is currently young and can't do many things yet.

The available commands for you to use are available below, using ~ prefix.'''
bot = commands.Bot(command_prefix='~', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(left : int, right : int):
    """I'll add two numbers together."""
    await bot.say(left + right)

@bot.command()
async def multiply(left : int, right : int):
	"""I will multiply two numbers."""
	await bot.say(left * right)

@bot.command()
async def roll(dice : str):
    """I will roll a dice for you. rolls:number"""
    try:
        rolls, limit = map(int, dice.split(':'))
    except Exception:
        await bot.say('Format has to be in rolls:number!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='I can let you help choose between multiple things')
async def choose(*choices : str):
    """I can let you help choose between multiple things"""
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating absolutely nothing...'):
    """I will repeat a message multiple times."""
    if times < 10:
        for i in range(times):
            await bot.say(content)
    else:
        await bot.say('I won\'t allow more than 10 repeats.')
@bot.command()
async def joined(member : discord.Member):
    """When someone new joins, I will tell you."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def sweet(ctx):
    """I will declare who is sweet"""
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not sweet'.format(ctx))

@sweet.command(name='Pink')
async def _bot():
    await bot.say('Yes, I\'m sweet.')

@sweet.command(name='Duse')
async def _bot():
    await bot.say('Yes, Duse\'s sweet.')

bot.run('discordpinkbot@gmail.com', 'hunter2')