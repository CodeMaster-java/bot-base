import disnake
from disnake.ext import commands
from disnake import Option, OptionType

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ticket", description="Envia uma mensagem com um botão para abrir um novo ticket")
    async def ticket(self, inter):
        await inter.response.send_message(
            content="Clique no botão abaixo para abrir um novo ticket",
            components=[
                disnake.ui.ActionRow(
                    disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Abrir Ticket")
                )
            ]
        )

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.label == "Abrir Ticket":
            guild = inter.guild
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                inter.user: disnake.PermissionOverwrite(read_messages=True)
            }
            ticket_channel = await guild.create_text_channel(f'ticket-{inter.user.name}', overwrites=overwrites)
            await ticket_channel.send(
                content=f"Ticket aberto por {inter.user.mention}",
                components=[
                    disnake.ui.ActionRow(
                        disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Fechar ticket")
                    )
                ]
            )

        elif inter.component.label == "Fechar ticket":
            await inter.channel.delete()

def setup(bot):
    bot.add_cog(TicketCog(bot))