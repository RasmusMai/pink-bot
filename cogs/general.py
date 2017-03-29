from discord.ext import commands
import discord, asyncio
import os, re, time, random, datetime, pprint, pickle
import urllib.request, urllib.parse, praw, json
from .utils import checks

class General:
    """General commands"""

    def __init__(self, bot):
        self.bot = bot
        with open('credentials.json') as f:
            self.weather_key = json.load(f)['openweathermap']

    @commands.command(hidden=True)
    async def ping(self):
        await self.bot.say("pong")

    @commands.command(pass_context=True, hidden=True)
    @checks.is_nsfw()
    async def nsfwping(self, ctx):
        await self.bot.say("nsfwpong")

    @commands.command()
    async def sourcecode(self):
        '''Returns the link to my source code.'''
        await self.bot.say("My source code is available on github: https://github.com/RasmusMai/pink-bot")

    @commands.command(pass_context=True)
    async def youtube(self, ctx):
        '''Returns the first search result.
        Example: youtube Minecraft Lets Play'''
        search_string = ctx.message.content.split(' ',1)[1]
        query_string = urllib.parse.urlencode({"search_query" : search_string})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        decoded = html_content.read().decode()
        if not re.search(r'href=\"\/watch\?v=(.{11})',decoded):
            await self.bot.say("I didn't find anything when searching for that.")
        else:
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', decoded)
            first_result = str("http://www.youtube.com/watch?v=" + search_results[0])
            await self.bot.say(first_result)

    @commands.command(pass_context=True)
    async def weather(self, ctx):
        '''Returns the current weather.
        Example: weather London or weather London, United Kingdom'''
        message = ctx.message
        location = message.content.split(' ',1)[1]
        if not re.search(r'^\w+$', location) and not re.search(r',', location):
            await self.bot.say("That's not a real place.")
            return
        try:
            weather_dict = self.get_weather(location.lower())
        except IndexError:
            await self.bot.say("Could you also specify a location? Example: `weather London` or `weather London, United Kingdom`")
            return
        if type(weather_dict) is str:
            await bot.say(weather_dict)
            return
        embed_color = discord.Colour(random.randint(0,16777215))
        icon_url = "http://openweathermap.org/img/w/" + str(weather_dict['weather'][0]['icon']) + ".png"
        data = discord.Embed(description="Lat: "+str(weather_dict['coord']['lat'])+", Lon: "+str(weather_dict['coord']['lon']), colour=embed_color)
        data.set_author(name=str(weather_dict['name']) + ", " + str(weather_dict['sys']['country']), url="http://openweathermap.com/city/"+str(weather_dict['id']))
        data.set_thumbnail(url=icon_url)
        data.add_field(name="Condition", value=weather_dict['weather'][0]['main'])
        data.add_field(name="Temperature", value=str(weather_dict['main']['temp']) +"°F" if location.split(' ',1)[0] == "f" or location.split(' ',1)[0] == "fahrenheit" else str(weather_dict['main']['temp'])+"°C")
        try:
            #if you thought the way I handled temperature was bad, check this out
            data.add_field(name="Wind", value=str(weather_dict['wind']['speed'])+"mph "+ str(weather_dict['wind']['deg'])+"°" if location.split(' ',1)[0] == "f" or location.split(' ',1)[0] == "fahrenheit" else str(weather_dict['wind']['speed']) + "m/s " + str(weather_dict['wind']['deg'])+"°")
        except:
            data.add_field(name="Wind", value="Unknown")
        try:
            data.add_field(name="Humidity", value=str(weather_dict['main']['humidity'])+"%")
        except:
            data.add_field(name="Humidity", value="Unknown")
        await self.bot.say(embed=data)

    def get_weather(self, location):
        if location.split(' ',1)[0] == 'f' or location.split(' ',1)[0] == 'fahrenheit':
            units = 'imperial'
            location = location.split(' ',1)[1]
        else:
            if location.split(' ',1)[0] == 'c' or location.split(' ',1)[0] == "celsius":
                location = location.split(' ',1)[1]
            units = 'metric'
        location = urllib.parse.quote_plus(location)
        try:
            if ', ' in location or ',' in location:
                global weather_key
                city = (location.split(',',1)[0]).strip(' ')
                country = (location.split(',',1)[1]).strip(' ')
                return json.loads(urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?q="+city+","+country+"&APPID="+self.weather_key+"&units="+units+"").read().decode())
            else:
                return json.loads(urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?q="+location+"&APPID="+self.weather_key+"&units="+units+"").read().decode())
        except urllib.error.HTTPError as err:
            if err.code == 502 or err.code == 404:
                return "Couldn't find a location with that name. The command should look like `weather London` or `weather London, United Kingdom`"
            else:
                raise

    def get_youtube(self, search_string):
        try:
            query_string = urllib.parse.urlencode({"search_query" : search_string})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            first_result = "http://www.youtube.com/watch?v=" + search_results[0]
            return first_result
        except IndexError:
            return ("I found nothing when searching for that.")

def setup(bot):
    bot.add_cog(General(bot))
