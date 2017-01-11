import discord, random, os, re, urllib.request, urllib.parse, argparse, pickle, asyncio, time, praw, datetime, json
from discord.ext import commands
clear = lambda: os.system('clear')

global description
description = '''```Hey, I'm Pink.
Born from severe crippling depression in addition to autism.

I can help you with:
• pinkhelp						      Shows this message
• youtube <string>					  Searches for a youtube video and returns the first result
• color/colour <string>			     Changes your color role to a requested value, use none for no colour.
• 8ball								 Ask the magic eight ball
• cat/kitty/neko						Returns a picture of a cat from random.cat
• dog/doggo/pupper					  Returns a picture of a dog from r/woofbarkwoof or r/woof_irl
• getoverwatch <battletag> <region>	 Returns an Overwatch profile. Region is optional, if none set I'll choose US. Case-sensitive.

Both cat and dog have a 5 second cooldown timer, to prevent abuse.
Currently, you can only search for one Overwatch profile at a time, because the server it contacts for those is terribly slow. Could take up to 30 seconds to finish the task.
If not otherwise mentioned, my commands aren't case sensitive.```'''
parser = argparse.ArgumentParser()
parser.add_argument("-t","--token")
parser.add_argument("-r","--reddit")
args = parser.parse_args()
reddit_secret = args.reddit
token = args.token

try:
	reddit = praw.Reddit(client_id='Hw0NlRx5TJoGkg',
				 client_secret=reddit_secret,
				 user_agent='pink.py Discord bot by /u/leeroyest')
	if reddit.read_only:
		print ("Reddit connected")
except:
	print ("Reddit connection failed")
bot = commands.Bot(command_prefix='~', description=description, category='category', pm_help=True)
last_sent_time = time.time()

global getoverwatch_working
getoverwatch_working = False

@bot.event
async def on_ready():
	clear()
	#last_message = ''
	print('I\'m starting up! My username is {}'.format(bot.user.name))
	print('My id - {}'.format(bot.user.id))
	print('------')
	await bot.change_presence(game=discord.Game(name = 'Use `pinkhelp`'))

@bot.event
async def on_message(message):
	time_now = str(datetime.datetime.now())
	#Checks that Pink won't reply to herself
	message_content = message.content.strip('\n').lower()

	if message.author == bot.user:
		return

	global description
	if message_content == "pinkhelp":
		await bot.send_message(message.author, description)
		print ("Messaged " + message.author.name + " to offer help.")

	global getoverwatch_working
	#Sends a picture of a dog from reddit
	if message_content == "dog" or message_content == "pupper" or message_content == "doggo":
		if time_passed(5):
			await bot.send_typing(message.channel)
			dogarray = []
			for submission in reddit.subreddit('woofbarkwoof').hot(limit=20):
				file_format = submission.url[-4:]
				if file_format.endswith('.jpg') or file_format.endswith('.png') or file_format.endswith('.gif'):
					dogarray.append(submission.url)
			for submission in reddit.subreddit('woof_irl').hot(limit=20):
				file_format = submission.url[-4:]
				if file_format.endswith('.jpg') or file_format.endswith('.png') or file_format.endswith('.gif'):
					dogarray.append(submission.url)
			dog_number = str(random.randint(100,999))
			chosen_dog = random.choice(dogarray)
			urllib.request.urlretrieve(chosen_dog,"woofbarkwoof/"+dog_number+chosen_dog[-4:])
			dog_to_be_sent = dog_number + chosen_dog[-4:]
			'''for item in os.listdir("woofbarkwoof"):
				dogarray.append(item)'''
			await bot.send_file(message.channel, "woofbarkwoof/"+dog_to_be_sent)
			print (time_now + " -- Sent dog")
	#Searches youtube for the keyword and returns the first result
	if message_content.startswith("youtube "):
		try:
			bot.send_typing(message.channel)
			query_string = urllib.parse.urlencode({"search_query" : message.content.split(' ', 1)[1]})
			html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
			search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
			first_result = "http://www.youtube.com/watch?v=" + search_results[0]
			await bot.send_message(message.channel,first_result)
			print (time_now + " -- Sent a youtube video: \""+ message.content.split(' ', 1)[1] +"\"")
		except IndexError:
			await bot.send_message(message.channel, "I found nothing when searching for that.")
		return
	if message_content == 'cat' or message_content == 'kitty' or message_content == 'neko':
		if time_passed(5):
			await bot.send_typing(message.channel)
			try:
				html_content = urllib.request.urlopen("http://random.cat/meow")
				html_content = html_content.read().decode()[:-2]
				picture_to_download = re.search(r"([-\w]+\.(jpg|png|gif|bmp))", html_content)
				picture_to_download = picture_to_download.group(1)
				urllib.request.urlretrieve("http://random.cat/i/"+picture_to_download,"temporary/"+picture_to_download)
				last_sent_time = time.time()
				print (time_now + " -- Sent a random.cat")
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

	if message_content == "shutdown pink" and allowed(message.author.id):
		await bot.change_presence(status=discord.Status.offline)
		exit()

	#A meme command, no use
	if message_content.startswith('8ball') or message_content == '8ball':
		await bot.send_typing(message.channel)
		await asyncio.sleep(3)
		eightball_array = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it', 'As I see, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'The stars say no', 'Outlook not so good', 'Very doubtful']
		await  bot.send_message(message.channel, random.choice(eightball_array))
		print (time_now + " -- 8ball")
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
			print (time_now + " -- Changing the color of " + message.author.name + " to " + requested_color)
		else:
			await bot.send_message(message.channel,"I can only give you one of the following colors: red, blue, green, purple, orange, yellow, grey and brown.")
		return

	#overwatch thingy hlep me
	try:
		if message_content.startswith('getoverwatch') and message_content.split(' ')[1]:
			if getoverwatch_working:
				await bot.send_message(message.channel, "I can only do one `getoverwatch` at a time until a bug is fixed!")
				return
			if '#' not in message.content.split(' ')[1]:
				await bot.send_message(message.channel, "Please use the correct format for the battletag `Thatnewguy#1790`")
				return
			ow_battletag = message.content.split(' ')[1].replace('#','-')
			try:
				ow_region = message_content.split(' ')[2]
			except IndexError:
				ow_region = 'us'
			supported_regions = ['us', 'eu', 'kr', 'cn']
			if ow_region not in supported_regions:
				await bot.send_message(message.channel, "Supported regions are `eu`, `us`, `kr` and `cn`")
				return
			await bot.send_typing(message.channel)
			print ("Getting Overwatch profile: " + ow_battletag)
			start_time = time.time()
			getoverwatch_working = True
			profile_call = 'https://api.lootbox.eu/pc/'+ow_region+'/'+ow_battletag+'/profile'
			heroes_call = 'https://api.lootbox.eu/pc/'+ow_region+'/'+ow_battletag+'/competitive/heroes'
			profile_dict = json.loads(urllib.request.urlopen(profile_call).read().decode())
			heroes_dict = json.loads(urllib.request.urlopen(heroes_call).read().decode())
			ow_won = int(profile_dict['data']['games']['competitive']['wins'])
			ow_lost = int(profile_dict['data']['games']['competitive']['lost'])
			ow_tied = int(profile_dict['data']['games']['competitive']['played']) - (ow_won + ow_lost)
			embed_color = discord.Colour(random.randint(0,16777215))
			data = discord.Embed(description='Platform: PC | Region: '+ow_region.upper(), colour=embed_color)
			data.set_author(name=message.content.split(' ')[1], url='http://masteroverwatch.com/profile/pc/'+ow_region+'/'+ow_battletag)
			data.set_thumbnail(url=profile_dict['data']['avatar'])
			data.add_field(name="Level", value=profile_dict['data']['level'])
			data.add_field(name="Playtime", value=profile_dict['data']['playtime']['quick'])
			data.add_field(name="Competitive Rating", value=profile_dict['data']['competitive']['rank'])
			data.add_field(name='Won/Lost/Tied', value=str(ow_won)+'/'+str(ow_lost)+'/'+str(ow_tied))
			data.add_field(name="Most Played Heroes", value=heroes_dict[1]['name'] + ', ' + heroes_dict[2]['name'] + ' and ' + heroes_dict[3]['name'])
			#data.set_image('https://i.imgur.com/aWkpX3W.png')
			finish_time = time.time()
			print ("It took " + str(finish_time - start_time) + " seconds to download the Overwatch profile.")
			getoverwatch_working = False
			await bot.send_message(message.channel,embed=data)
			return
	except IndexError:
		await bot.send_message(message.channel, 'Please use `getoverwatch <battletaghere> <eu/us>` If no region is provided it\'ll use `us`')
		return

	#Scans the message for trigger words
	msg_array = message.content.split()
	for word in msg_array:
		if word.lower() == "weeb" or word.lower() == "weeaboo":
			print(time_now + " -- " + message.author.name + " said weeb!")
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
	await bot.send_message(Member.server, Member.mention + " has joined at " + Member.joined_at + ". Please state your name and purpose.")
@bot.event
async def on_member_remove(Member):
	await bot.send_message(Member.server, Member.mention + " has left :o")

@asyncio.coroutine
def call_to_dict(api_call):
	html_content = yield from urllib.request.urlopen(api_call)
	response_string = html_content.read().decode()
	json_dict = json.loads(response_string)
	return json_dict

#If called, it checks if the message.author has permissions. The list of people with administrative rights are stored in allowed_users.dat as id
def allowed(msg_id):
	allowed_file = "allowed_users.dat";
	allowed_array = []
	with open("allowed_users.dat", "r") as users:
		for user in users:
			if user.strip("\n") == msg_id:
				return True
	return False

global time_last_sent
time_last_sent = 0.0
def time_passed(condition):
	global time_last_sent
	current_time = time.time()
	#print ("time passed: "+ str(current_time - time_last_sent))
	if current_time - time_last_sent > condition:
		time_last_sent = time.time()
		return True
	else:
		return False

#265442795446075397
#https://discordapp.com/oauth2/authorize?client_id=265442795446075397&scope=bot&permissions=0

bot.login('token')
bot.run(token)
