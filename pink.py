import discord, random, getpass, os
from discord.ext import commands
clear = lambda: os.system('cls')

description = '''Pink - Your general purpose Discord friend.
I'm is currently young and can't do many things yet.

The available commands for you to use are available below, using ~ prefix.'''
bot = commands.Bot(command_prefix='~', description=description, category='category', pm_help=True)

@bot.event
async def on_ready():
	clear()
	print('I\'m starting up! My username is {}'.format(bot.user.name))
	print('My id - {}'.format(bot.user.id))
	print('------')
	await bot.change_status(discord.Game(name = 'Type ~help for info'))

@bot.command()
async def changestatus(message):
	'''Change my game name'''
	await bot.say(message)
	'''
	if message.author == bot.user:
		return
	if message.content.startswith('~status'):
		if message.author == discord.User(name = 'Rasmus'):
			new_status = message.content[8:]
			await bot.change_status(discord.Game(name = new_status))
			await bot.send_message(message.channel, 'I am now playing {}'.format(new_status))
		else:
			await bot.send_message(message.channel, 'I\'m afraid you can\'t do that.')
	'''
@bot.command()
async def add(left : int, right : int):
	"""I'll add two numbers together."""
	await bot.say("{} + {} = {}".format(left,right,left+right))
	print('Adding {} and {}'.format(left, right))

@bot.command()
async def subtract(left : int, right : int):
	"""I'll subtract two numbers."""
	await bot.say("{} - {} = {}".format(left,right,left-right))
	print('Subtracting {} and {}')
	
@bot.command()
async def multiply(left : int, right : int):
	"""I will multiply two numbers."""
	await bot.say("{} * {} = {}".format(left, right, left*right))
	print('Multiplying {} and {}'.format(left,right))

@bot.command()
async def divide(left : int, right : int):
	"""I will divide two numbers."""
	if right == 0:
		await bot.say("{} / {} = ∞".format(left, right))
	else:
		await bot.say("{} / {} = {}".format(left, right, left/right))
	print('Dividing {} and {}'.format(left,right))

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
	print('Someone rolled {}'.format(result))

@bot.command(description='I can let you help choose between multiple things')
async def choose(*choices : str):
	"""I can let you help choose between multiple things"""
	await bot.say(random.choice(choices))
	print('I have just made a choice')

@bot.command()
async def repeat(times : int, content='repeating absolutely nothing...'):
	"""I will repeat a message multiple times."""
	if times < 10:
		print ('I just repeated {} {} times'.format(content, times))
		for i in range(times):
			await bot.say(content)
	else:
		await bot.say('I won\'t allow more than 10 repeats.')

@bot.command()
async def joined(member : discord.Member):
	"""When someone new joins, I will tell you."""
	await bot.say('**{0.name}** joined in {0.joined_at}'.format(member))
	print ('{0.name} joined in {0.joined_at}'.format(member))
	
@bot.group(pass_context=True)
async def sweet(ctx):
	"""I will declare who is sweet"""
	if ctx.invoked_subcommand is None:
		await bot.say('No, {0.subcommand_passed} is not sweet'.format(ctx))

@sweet.command(name='Pink')
async def _bot():
	"""Is Pink cool?"""
	await bot.say('Yes, I\'m sweet.')
	print ('Yes!! Someone just wondered if I\'m sweet!')

@sweet.command(name='Duse')
async def _bot():
	"""Is Duse cool?"""
	await bot.say('Yes, Duse\'s sweet.')
auth = "auth.txt"
autharray = []
with open(auth) as file:
	for value in file.read().split(':'):
		autharray.append(value)
if len(autharray) > 1:
	email = autharray[0]
	pswd = autharray[1]
else:
	print ('---No auth.txt detected or empty---')
	email = input('Email ==> ')
	pswd = getpass.getpass('Password ==> ')
bot.run(email,pswd)