from discord.ext import commands
from urllib.error import HTTPError
import urllib.request
import json


class Piston(commands.Cog):
    """https://github.com/engineer-man/piston"""

    BASE_URL = "https://emkc.org/api/v1/piston"
    VERSIONS_URL = "https://emkc.org/api/v1/piston/versions"
    EXECUTE_URL = "https://emkc.org/api/v1/piston/execute"

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def parse_message(message):
        lines = message.split('\n')
        if ' ' in lines[0]:  # language is specified with command
            language = lines[0].split(' ')[1]
        else:
            language = lines[1].replace('`', '')  # language is hopefully specified in the code block
        if len(lines) == 1:
            code = lines[0].split(' ', 2)[-1]  # is entirely contained within a single line
        else:
            # is multiline, also clean code block
            code = ''.join([line for line in lines[1:] if not line.startswith('```')])
        return language, code

    @commands.command(name="execute", description="oh no")
    async def execute_code(self, ctx):
        """monke OOH OOH AAH AAH."""
        response = ''
        message = ctx.message.content
        language, code = self.parse_message(message)
        payload = {'language': language, 'source': code}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.EXECUTE_URL)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Content-Length', str(len(data)))
        try:
            api_response = urllib.request.urlopen(req, data)
            json_response = json.loads(api_response.read().decode('utf-8'))
            response = json_response['output']
        except HTTPError as err:
            await ctx.send(f"HTTP Error while querying Piston: {err.code}\n{err.read().decode()}")
            return
        await ctx.send(response)


def setup(bot):
    bot.add_cog(Piston(bot))
