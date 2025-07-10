"""
Cog de comandos de moderação
"""

import disnake
import asyncio
from datetime import datetime, timedelta
from disnake.ext import commands
from utils import EmbedUtils, BotUtils
from config import BotConfig

class ModerationCog(commands.Cog):
    """Comandos de moderação do servidor"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="kick",
        description="Expulsa um usuário do servidor"
    )
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        inter,
        user: disnake.Member = commands.Param(description="Usuário para expulsar"),
        reason: str = commands.Param(description="Motivo da expulsão", default="Não especificado")
    ):
        """Comando para expulsar usuários"""
        
        # Verificações de segurança
        if user == inter.author:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Você não pode expulsar a si mesmo!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        if user.top_role >= inter.author.top_role:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Você não pode expulsar alguém com cargo igual ou superior ao seu!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        if user.top_role >= inter.guild.me.top_role:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não posso expulsar alguém com cargo igual ou superior ao meu!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Tentar enviar DM antes de expulsar
        try:
            dm_embed = EmbedUtils.warning_embed(
                title="Você foi expulso!",
                description=f"Você foi expulso do servidor **{inter.guild.name}**"
            )
            dm_embed.add_field(name="Motivo", value=reason, inline=False)
            dm_embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            await user.send(embed=dm_embed)
        except:
            pass
        
        # Expulsar usuário
        try:
            await user.kick(reason=f"Expulso por {inter.author} - {reason}")
            
            embed = EmbedUtils.success_embed(
                title="Usuário expulso",
                description=f"**{user.display_name}** foi expulso do servidor"
            )
            embed.add_field(name="Motivo", value=reason, inline=False)
            embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            
            await inter.response.send_message(embed=embed)
            
        except disnake.Forbidden:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não tenho permissão para expulsar este usuário!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
    
    @commands.slash_command(
        name="ban",
        description="Bane um usuário do servidor"
    )
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        inter,
        user: disnake.Member = commands.Param(description="Usuário para banir"),
        reason: str = commands.Param(description="Motivo do banimento", default="Não especificado"),
        delete_days: int = commands.Param(description="Dias de mensagens para deletar (0-7)", default=0, min_value=0, max_value=7)
    ):
        """Comando para banir usuários"""
        
        # Verificações de segurança
        if user == inter.author:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Você não pode banir a si mesmo!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        if user.top_role >= inter.author.top_role:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Você não pode banir alguém com cargo igual ou superior ao seu!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        if user.top_role >= inter.guild.me.top_role:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não posso banir alguém com cargo igual ou superior ao meu!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Tentar enviar DM antes de banir
        try:
            dm_embed = EmbedUtils.error_embed(
                title="Você foi banido!",
                description=f"Você foi banido do servidor **{inter.guild.name}**"
            )
            dm_embed.add_field(name="Motivo", value=reason, inline=False)
            dm_embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            await user.send(embed=dm_embed)
        except:
            pass
        
        # Banir usuário
        try:
            await user.ban(reason=f"Banido por {inter.author} - {reason}", delete_message_days=delete_days)
            
            embed = EmbedUtils.success_embed(
                title="Usuário banido",
                description=f"**{user.display_name}** foi banido do servidor"
            )
            embed.add_field(name="Motivo", value=reason, inline=False)
            embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            if delete_days > 0:
                embed.add_field(name="Mensagens deletadas", value=f"{delete_days} dias", inline=False)
            
            await inter.response.send_message(embed=embed)
            
        except disnake.Forbidden:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não tenho permissão para banir este usuário!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
    
    @commands.slash_command(
        name="unban",
        description="Remove o banimento de um usuário"
    )
    @commands.has_permissions(ban_members=True)
    async def unban(
        self,
        inter,
        user_id: str = commands.Param(description="ID do usuário para desbanir"),
        reason: str = commands.Param(description="Motivo do desbanimento", default="Não especificado")
    ):
        """Comando para desbanir usuários"""
        
        try:
            user_id = int(user_id)
        except ValueError:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="ID do usuário inválido!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Verificar se o usuário está banido
        banned_users = [ban_entry async for ban_entry in inter.guild.bans()]
        banned_user = None
        
        for ban_entry in banned_users:
            if ban_entry.user.id == user_id:
                banned_user = ban_entry.user
                break
        
        if not banned_user:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Usuário não encontrado na lista de banidos!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Desbanir usuário
        try:
            await inter.guild.unban(banned_user, reason=f"Desbanido por {inter.author} - {reason}")
            
            embed = EmbedUtils.success_embed(
                title="Usuário desbanido",
                description=f"**{banned_user.display_name}** foi desbanido do servidor"
            )
            embed.add_field(name="Motivo", value=reason, inline=False)
            embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            
            await inter.response.send_message(embed=embed)
            
        except disnake.Forbidden:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não tenho permissão para desbanir usuários!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
    
    @commands.slash_command(
        name="timeout",
        description="Coloca um usuário em timeout"
    )
    @commands.has_permissions(moderate_members=True)
    async def timeout(
        self,
        inter,
        user: disnake.Member = commands.Param(description="Usuário para colocar em timeout"),
        duration: int = commands.Param(description="Duração em minutos (max 2880)", min_value=1, max_value=2880),
        reason: str = commands.Param(description="Motivo do timeout", default="Não especificado")
    ):
        """Comando para colocar usuários em timeout"""
        
        # Verificações de segurança
        if user == inter.author:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Você não pode colocar a si mesmo em timeout!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        if user.top_role >= inter.author.top_role:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Você não pode colocar alguém com cargo igual ou superior ao seu em timeout!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Calcular tempo de timeout
        timeout_until = datetime.utcnow() + timedelta(minutes=duration)
        
        # Aplicar timeout
        try:
            await user.timeout(until=timeout_until, reason=f"Timeout por {inter.author} - {reason}")
            
            embed = EmbedUtils.warning_embed(
                title="Usuário em timeout",
                description=f"**{user.display_name}** foi colocado em timeout"
            )
            embed.add_field(name="Duração", value=f"{duration} minutos", inline=False)
            embed.add_field(name="Até", value=f"<t:{int(timeout_until.timestamp())}:F>", inline=False)
            embed.add_field(name="Motivo", value=reason, inline=False)
            embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            
            await inter.response.send_message(embed=embed)
            
        except disnake.Forbidden:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não tenho permissão para colocar este usuário em timeout!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
    
    @commands.slash_command(
        name="untimeout",
        description="Remove o timeout de um usuário"
    )
    @commands.has_permissions(moderate_members=True)
    async def untimeout(
        self,
        inter,
        user: disnake.Member = commands.Param(description="Usuário para remover timeout"),
        reason: str = commands.Param(description="Motivo da remoção", default="Não especificado")
    ):
        """Comando para remover timeout de usuários"""
        
        if not user.is_timed_out():
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Este usuário não está em timeout!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Remover timeout
        try:
            await user.timeout(until=None, reason=f"Timeout removido por {inter.author} - {reason}")
            
            embed = EmbedUtils.success_embed(
                title="Timeout removido",
                description=f"Timeout de **{user.display_name}** foi removido"
            )
            embed.add_field(name="Motivo", value=reason, inline=False)
            embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            
            await inter.response.send_message(embed=embed)
            
        except disnake.Forbidden:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não tenho permissão para remover timeout deste usuário!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
    
    @commands.slash_command(
        name="clear",
        description="Limpa mensagens do canal"
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(
        self,
        inter,
        amount: int = commands.Param(description="Quantidade de mensagens para limpar (max 100)", min_value=1, max_value=100),
        user: disnake.Member = commands.Param(description="Limpar apenas mensagens de um usuário específico", default=None)
    ):
        """Comando para limpar mensagens"""
        
        await inter.response.defer()
        
        def check(message):
            if user:
                return message.author == user
            return True
        
        try:
            deleted = await inter.channel.purge(limit=amount, check=check)
            
            embed = EmbedUtils.success_embed(
                title="Mensagens limpas",
                description=f"**{len(deleted)}** mensagens foram deletadas"
            )
            
            if user:
                embed.add_field(name="Usuário", value=user.mention, inline=False)
            
            embed.add_field(name="Canal", value=inter.channel.mention, inline=False)
            embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            
            # Enviar mensagem temporária
            msg = await inter.followup.send(embed=embed)
            
            # Deletar após 5 segundos
            await BotUtils.safe_delete_message(msg, 5)
            
        except disnake.Forbidden:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não tenho permissão para deletar mensagens!"
            )
            await inter.followup.send(embed=embed)
    
    @commands.slash_command(
        name="warn",
        description="Avisa um usuário"
    )
    @commands.has_permissions(moderate_members=True)
    async def warn(
        self,
        inter,
        user: disnake.Member = commands.Param(description="Usuário para avisar"),
        reason: str = commands.Param(description="Motivo do aviso")
    ):
        """Comando para avisar usuários"""
        
        # Tentar enviar DM
        try:
            dm_embed = EmbedUtils.warning_embed(
                title="Você recebeu um aviso!",
                description=f"Você recebeu um aviso no servidor **{inter.guild.name}**"
            )
            dm_embed.add_field(name="Motivo", value=reason, inline=False)
            dm_embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            await user.send(embed=dm_embed)
            dm_sent = True
        except:
            dm_sent = False
        
        embed = EmbedUtils.warning_embed(
            title="Usuário avisado",
            description=f"**{user.display_name}** recebeu um aviso"
        )
        embed.add_field(name="Motivo", value=reason, inline=False)
        embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
        embed.add_field(name="DM enviada", value="Sim" if dm_sent else "Não", inline=False)
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="slowmode",
        description="Define o modo lento do canal"
    )
    @commands.has_permissions(manage_channels=True)
    async def slowmode(
        self,
        inter,
        seconds: int = commands.Param(description="Segundos de slowmode (0 para desativar)", min_value=0, max_value=21600)
    ):
        """Comando para definir slowmode"""
        
        try:
            await inter.channel.edit(slowmode_delay=seconds)
            
            if seconds == 0:
                embed = EmbedUtils.success_embed(
                    title="Slowmode desativado",
                    description="O modo lento foi desativado neste canal"
                )
            else:
                embed = EmbedUtils.success_embed(
                    title="Slowmode ativado",
                    description=f"Modo lento definido para **{seconds}** segundos"
                )
            
            embed.add_field(name="Canal", value=inter.channel.mention, inline=False)
            embed.add_field(name="Moderador", value=inter.author.mention, inline=False)
            
            await inter.response.send_message(embed=embed)
            
        except disnake.Forbidden:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não tenho permissão para editar este canal!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationCog(bot))
