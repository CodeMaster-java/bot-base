import disnake
from disnake.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='ping',
        description='Verifica a latência do bot.'
    )
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # Convertendo para milissegundos


        embed = disnake.Embed(
            title='Pong! 🏓',
            description=f'Latência: {latency}ms',
            color=disnake.Color.blue()
        )

        await ctx.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(PingCog(bot))
