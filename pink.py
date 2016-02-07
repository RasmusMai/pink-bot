import discord
from discord.ext import commands
import random

description = '''Pink - Your general purpose Discord bot.
She is currently young and can't do many things yet.

The available commands for Pink are available below, using * prefix.'''
bot = commands.Bot(command_prefix='*', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def multiply(left : int, right : int):
	"""Multiplies two numbers."""
	await bot.say(left * right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice. rolls:number"""
    try:
        rolls, limit = map(int, dice.split(':'))
    except Exception:
        await bot.say('Format has to be in rolls:number!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
	if times 
    for i in range(times):
        await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='Pink')
async def _bot():
    """Is Pink cool?"""
    await bot.say('Yes, I\'m cool.')

@cool.command(name='Duse')
async def _bot():
    """Is Pink cool?"""
    await bot.say('Yes, Duse\'s cool.')

bot.run('email', 'password')