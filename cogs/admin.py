from discord.ext import commands
from .utils import checks


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True, name="nickname")
    #@checks.is_admin()
    async def change_nickname(self, ctx, target_name: str):
        if target_name == 'none':
            await ctx.guild.me.edit(nick=None)
        else:
            await ctx.guild.me.edit(nick=target_name)


def setup(bot):
    bot.add_cog(Admin(bot))
