from discord.ext import commands
import markovify
import time

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def ping(self, ctx):
        await ctx.send("pong")


    @commands.command()
    async def studentcount(self, ctx):
        await ctx.send("many")

    @commands.command(pass_context=True)
    async def markov(self, ctx):
        '''Generates sentences up to 140 characters.
        The text for titles/comments/text-posts are generated using "markov chains", a random process that's "trained" from looking at real data. If you've ever used a keyboard on your phone that tries to predict which word you'll type next, those are often built using something similar.

        Basically, you feed in a bunch of sentences, and even though it has no understanding of the meaning of the text, it picks up on patterns like "word A is often followed by word B". Then when you want to generate a new sentence, it "walks" its way through from the start of a sentence to the end of one, picking sequences of words that it knows are valid based on that initial analysis. So generally short sequences of words in the generated sentences will make sense, but often not the whole thing. It's taught by messages that are being sent in the same server. All messages are stored anonymously.

        A more detailed explanation: http://www.reddit.com/r/Python/comments/2ife6d/pykov_a_tiny_python_module_on_finite_regular/cl3bybj'''
        start_time = time.time()
        with open('markov/' + str(ctx.message.guild.id) + '.txt', 'r+', encoding="utf8") as f:
            text = f.read()
            f.seek(0)
            f.truncate()
            f.write(text)
        text_model = markovify.NewlineText(text)
        try:
            await ctx.send(text_model.make_short_sentence(140))
        except:
            await ctx.send("I failed to generate a sentence, might need more data to study on.")
        end_time = time.time()
        diff_time = end_time - start_time
        print("Markov took - " + str(diff_time))


def setup(bot):
    bot.add_cog(General(bot))
