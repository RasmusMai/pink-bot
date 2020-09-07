from discord.ext import commands
import random

class Rofoc(commands.Cog):

    bean_links = ["https://www.bbcgoodfood.com/recipes/easy-beef-burritos",
                  "https://www.recipetineats.com/beef-burritos/",
                  "https://www.theseasonedmom.com/easiest-burrito-recipe/",
                  "https://www.tasteofhome.com/recipes/tasty-burritos/"]

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="B")
    async def nikki_b(self, ctx):
        await ctx.send("B")

    @commands.command(name="bean")
    async def dave_bean(self, ctx):
        choice = random.choice(self.bean_links)
        await ctx.send(choice)


def setup(bot):
    bot.add_cog(Rofoc(bot))