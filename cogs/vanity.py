from discord.ext import commands
import discord, asyncio
from .utils import checks
import os, re, time, threading, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json, markovify

class Vanity:
    '''Commands with no purpose, but to entertain.'''

    def __init__(self, bot):
        self.bot = bot
        self.eightball_array = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it',
        'As I see, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later',
        'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'The stars say no',
        'Outlook not so good', 'Very doubtful']
        self.catfacts_file = 'catfacts.json'
        self.markov_json = 'markov.json'
        if not os.path.isfile(self.catfacts_file):
            with open (self.catfacts_file, 'w') as f:
                f.write('{"enabled_servers":[]')
        self.command_list = ['8ball', 'subreddit', 'youtube', 'addblacklist', 'removeblacklist', 'addpermissions', 'removepermissions', 'weather', 'color', 'colour']

    async def catfacts_loop():
        response = json.loads(urllib.request.urlopen("https://catfacts-api.appspot.com/api/facts").read().decode())
        with open (catfacts_file, 'r') as f:
            catfacts = json.load(f)
            for server in self.bot.servers:
                if server.id in catfacts['enabled_servers']:
                    await self.bot.send_message(server, catfacts['facts'][0])
        threading.Timer(86400, catfacts_loop).start()

    @commands.command(name="8ball")
    async def _8ball(self):
        '''Ask the magic eight ball anything.'''
        await self.bot.say(random.choice(self.eightball_array))

    '''
        @commands.command(pass_context=True)
        @checks.is_admin()
        async def togglecatfacts(self):
            with open (self.catfacts_file, 'r') as f:
                catfacts = json.load(f)
                if str(server.id) not in catfacts['enabled_servers']:
                    catfacts['enabled_servers'].append(str(server.id))
                    await self.bot.say("Catfacts have been enabled for this server.")
                else:
                    catfacts['enabled_servers'].remove(str(server.id))
                    await self.bot.say("Catfacts have been disabled for this server.")
            with open (self.catfacts_file, 'w') as f:
                json.dump(catfacts,f,sort_keys = True,indent = 4)
    '''

    @commands.command(pass_context=True)
    async def markov(self, ctx):
        '''Generates sentences up to 140 characters.
        The text for titles/comments/text-posts are generated using "markov chains", a random process that's "trained" from looking at real data. If you've ever used a keyboard on your phone that tries to predict which word you'll type next, those are often built using something similar.

        Basically, you feed in a bunch of sentences, and even though it has no understanding of the meaning of the text, it picks up on patterns like "word A is often followed by word B". Then when you want to generate a new sentence, it "walks" its way through from the start of a sentence to the end of one, picking sequences of words that it knows are valid based on that initial analysis. So generally short sequences of words in the generated sentences will make sense, but often not the whole thing. It's taught by messages that are being sent in the same server. All messages are stored anonymously.

        A more detailed explanation: http://www.reddit.com/r/Python/comments/2ife6d/pykov_a_tiny_python_module_on_finite_regular/cl3bybj'''
        start_time = time.time()
        with open('markov/'+ctx.message.server.id+'.txt', 'r+') as f:
            text = f.read()
            for i in range(0,len(self.command_list)):
                text = text.replace(self.command_list[i]+' ', '')
            f.seek(0)
            f.truncate()
            f.write(text)
        text_model = markovify.NewlineText(text)
        try:
            await self.bot.say(text_model.make_short_sentence(140))
        except:
            await self.bot.say("I failed to generate a sentence, might need more data to study on.")
        end_time = time.time()
        diff_time = end_time - start_time
        print ("Markov took - "+str(diff_time))
def setup(bot):
    bot.add_cog(Vanity(bot))
