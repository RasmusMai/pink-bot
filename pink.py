import discord, random, os, re, urllib.request, urllib.parse, argparse, pickle, asyncio
from discord.ext import commands
clear = lambda: os.system('clear')

description = '''Pink - Your general purpose Discord friend.
I'm currently young and can't do many things yet.

The available commands for you to use are available below, using ~ prefix.'''
bot = commands.Bot(command_prefix='~', description=description, category='category', pm_help=True)

@bot.event
async def on_ready():
	clear()
	print('I\'m starting up! My username is {}'.format(bot.user.name))
	print('My id - {}'.format(bot.user.id))
	print('------')
	await bot.change_presence(game=discord.Game(name = 'Type ~help for info'))

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return;
	msg_array = message.content.split()
	for word in msg_array:
		if word.lower() == "weeb" or word.lower() == "weeaboo":
			print("Someone said weeb!")
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
			return
	if message.content.startswith("changepresence ") and allowed(message.author.id):
		print ('changing presence to '+ message.content.split(' ', 1)[1])
		await bot.change_presence(game=discord.Game(name = message.content.split(' ', 1)[1]))
		return
	if message.content.startswith("youtube "):
		query_string = urllib.parse.urlencode({"search_query" : message.content.split(' ', 1)[1]})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		first_result = "http://www.youtube.com/watch?v=" + search_results[0]
		await bot.send_message(message.channel,first_result)
		return
	if message.content.startswith('8ball') or message.content == '8ball':
		await bot.send_typing(message.channel)
		await asyncio.sleep(3)
		eightball_array = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it', 'As I see, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'The stars say no', 'Outlook not so good', 'Very doubtful']
		await  bot.send_message(message.channel, "The Magic 8-Ball has decided - " + random.choice(eightball_array))
	if message.content.startswith("color ") or message.content.startswith("colour "):
		possible_colors = ['red','blue','green','purple','orange','yellow','grey','brown']
		requested_color = message.content.split(' ', 1)[1]
		requested_color.lower()
		requested_color.strip()
		if requested_color in possible_colors:
			for server_role in message.server.roles:
				if server_role.name == requested_color:
					role_given = server_role
			for color in possible_colors:
				for current_role in message.author.roles:
					if current_role.name in possible_colors:
						await bot.remove_roles(message.author, current_role)
				if color in message.author.roles:
					pass
					#await bot.remove_roles(message.author,"nein")
			await bot.add_roles(message.author, role_given)
		else:
			await bot.send_message(message.channel,"I can only edit the following colors: red, blue, green, purple, orange, yellow, grey and brown.")
	await bot.process_commands(message)

@bot.event
async def on_member_join(Member):
	await bot.send_message(Member.server, Member.mention + " has joined. Please state your name and purpose.")
@bot.event
async def on_member_remove(Member):
	await bot.send_message(Member.server, Member.mention + " has left :o")

def allowed(msg_id):
	allowed_file = "allowed_users.dat";
	allowed_array = []
	with open("allowed_users.dat", "r") as users:
		for user in users:
			if user.strip("\n") == msg_id:
				return True
	return False

parser = argparse.ArgumentParser()
parser.add_argument("-t","--token")
args = parser.parse_args()
token = args.token
'''
try:
	auth = "auth.txt"
	autharray = []
	with open(auth, "r") as file:
		for value in file.read().split(':'):
			autharray.append(value)
	if len(autharray) > 0:
		token = autharray[0]
	#pswd = autharray[1]
	file.close()
except FileNotFoundError:
	print ('---No auth.txt detected or empty---')
	token = input('Token ==> ')

        #pswd = getpass.getpass('Password ==> ')
'''
#265442795446075397
#https://discordapp.com/oauth2/authorize?client_id=265442795446075397&scope=bot&permissions=0
bot.login('token')
bot.run(token)
