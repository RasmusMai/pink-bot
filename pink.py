import discord, random, os, re, urllib.request, urllib.parse, argparse, pickle, asyncio
from discord.ext import commands
clear = lambda: os.system('clear')

description = '''Pink - Your general purpose Discord friend.
Born from severe crippling depression in addition to autism.

I can help you with:
• youtube <string>					Searches for a youtube video and returns the first result
• color or colour <string>			Changes your color to a specified value.
• 8ball								Ask the magic eight ball
• cat/kitty/neko					Returns a picture of a cat from random.cat

My commands are not (at the very least, shouldn\'t be) case sensitive.'''
bot = commands.Bot(command_prefix='~', description=description, category='category', pm_help=True)

@bot.event
async def on_ready():
	clear()
	#last_message = ''
	print('I\'m starting up! My username is {}'.format(bot.user.name))
	print('My id - {}'.format(bot.user.id))
	print('------')
	#await bot.change_presence(game=discord.Game(name = 'Use `color <colorname>`'))

@bot.event
async def on_message(message):
	#Checks that Pink won't reply to herself
	message_content = message.content.strip('/n').lower()

	if message.author == bot.user:
		return

	#Searches youtube for the keyword and returns the first result
	if message_content.startswith("youtube "):
		query_string = urllib.parse.urlencode({"search_query" : message.content.split(' ', 1)[1]})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		first_result = "http://www.youtube.com/watch?v=" + search_results[0]
		await bot.send_message(message.channel,first_result)
		return
	if message_content == 'cat' or message_content == 'kitty' or message_content == 'neko':
		await bot.send_typing(message.channel)
		try:
			html_content = urllib.request.urlopen("http://random.cat/meow")
			html_content = html_content.read().decode()[:-2]
			picture_to_download = re.search(r"([-\w]+\.(jpg|png|gif|bmp))", html_content)
			picture_to_download = picture_to_download.group(1)
			urllib.request.urlretrieve("http://random.cat/i/"+picture_to_download,"temporary/"+picture_to_download)
			await bot.send_file(message.channel, 'temporary/'+picture_to_download)
		except:
			await bot.send_message(message.channel, "Sorry, I couldn't do it.")

	#People with permissions can change the presence of Pink
	if message_content.startswith("changepresence ") and allowed(message.author.id):
		print ('changing presence to '+ message_content.split(' ', 1)[1])
		await bot.change_presence(game=discord.Game(name = message_content.split(' ', 1)[1]))
		return

	#Deletes the last message sent by Pink.py
	if message_content.startswith('deletelast') or message_content == 'deletelast':
		if allowed(message.author.id):
			pass

	#A meme command, no use
	if message_content.startswith('8ball') or message_content == '8ball':
		await bot.send_typing(message.channel)
		await asyncio.sleep(3)
		eightball_array = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it', 'As I see, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'The stars say no', 'Outlook not so good', 'Very doubtful']
		await  bot.send_message(message.channel, random.choice(eightball_array))
		return

	#Self color changing
	#First, it checks if the color requested is in the list of possible colors.
	#Then it finds the server's equivalent for that color. It finds and matches the server role by name.
	#That automates the process and doesn't require storing of the server roles.
	#Lastly, it removes all other color roles from the requester and gives them the new one.
	if message_content.startswith("color ") or message_content.startswith("colour "):
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
							await bot.send_message(message.channel, "You already have that color")
							return
						await bot.remove_roles(message.author, current_role)
			if requested_color == 'none':
				await bot.send_message(message.channel, "You are now without a color. Doesn\'t it feel great to be different!")
			else:
				await bot.add_roles(message.author, role_given)
				await bot.send_message(message.channel,"Your color is now "+ requested_color)
			print ("Changing the color of " + message.author.name + " to " + requested_color)
		else:
			await bot.send_message(message.channel,"I can only give you one of the following colors: red, blue, green, purple, orange, yellow, grey and brown.")
		return

	#Scans the message for trigger words
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
	await bot.process_commands(message)
	return

#Reacts to and announces member joining or leaving
@bot.event
async def on_member_join(Member):
	await bot.send_message(Member.server, Member.mention + " has joined. Please state your name and purpose.")
@bot.event
async def on_member_remove(Member):
	await bot.send_message(Member.server, Member.mention + " has left :o")

#If called, it checks if the message.author has permissions. The list of people with administrative rights are stored in allowed_users.dat as id
def allowed(msg_id):
	allowed_file = "allowed_users.dat";
	allowed_array = []
	with open("allowed_users.dat", "r") as users:
		for user in users:
			if user.strip("\n") == msg_id:
				return True
	return False

#265442795446075397
#https://discordapp.com/oauth2/authorize?client_id=265442795446075397&scope=bot&permissions=0
parser = argparse.ArgumentParser()
parser.add_argument("-t","--token")
args = parser.parse_args()
token = args.token
bot.login('token')
bot.run(token)
