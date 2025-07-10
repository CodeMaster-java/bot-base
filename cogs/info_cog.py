"""
Cog de informações do bot e servidor
"""

import disnake
import platform
import psutil
from datetime import datetime
from disnake.ext import commands
from utils import EmbedUtils, BotUtils
from config import BotConfig

class InfoCog(commands.Cog):
    """Comandos de informações do bot e servidor"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="info",
        description="Mostra informações detalhadas do bot"
    )
    async def bot_info(self, inter):
        """Comando para mostrar informações do bot"""
        
        embed = EmbedUtils.create_embed(
            title="🤖 Informações do Bot",
            description=f"**{self.bot.user.name}** - Bot Discord moderno"
        )
        
        # Informações básicas
        embed.add_field(
            name="📝 Nome",
            value=self.bot.user.name,
            inline=True
        )
        
        embed.add_field(
            name="🆔 ID",
            value=self.bot.user.id,
            inline=True
        )
        
        embed.add_field(
            name="⏰ Criado em",
            value=f"<t:{int(self.bot.user.created_at.timestamp())}:F>",
            inline=True
        )
        
        # Estatísticas
        embed.add_field(
            name="🌐 Servidores",
            value=len(self.bot.guilds),
            inline=True
        )
        
        embed.add_field(
            name="👥 Usuários",
            value=len(self.bot.users),
            inline=True
        )
        
        embed.add_field(
            name="⚡ Comandos",
            value=len(self.bot.slash_commands),
            inline=True
        )
        
        # Performance
        embed.add_field(
            name="📡 Latência",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=True
        )
        
        embed.add_field(
            name="⏱️ Uptime",
            value=self.bot.get_uptime(),
            inline=True
        )
        
        embed.add_field(
            name="💾 RAM",
            value=f"{psutil.virtual_memory().percent}%",
            inline=True
        )
        
        # Tecnologias
        tech_info = (
            f"**Python:** {platform.python_version()}\n"
            f"**Disnake:** {disnake.__version__}\n"
            f"**Sistema:** {platform.system()} {platform.release()}"
        )
        
        embed.add_field(
            name="🔧 Tecnologias",
            value=tech_info,
            inline=False
        )
        
        # Links úteis
        embed.add_field(
            name="🔗 Links",
            value="[Convite](https://discord.com) • [Suporte](https://discord.com) • [GitHub](https://github.com)",
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Solicitado por {inter.author.display_name}")
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="serverinfo",
        description="Mostra informações do servidor atual"
    )
    async def server_info(self, inter):
        """Comando para mostrar informações do servidor"""
        
        guild = inter.guild
        
        embed = EmbedUtils.create_embed(
            title="🏠 Informações do Servidor",
            description=f"Informações sobre **{guild.name}**"
        )
        
        # Informações básicas
        embed.add_field(
            name="📝 Nome",
            value=guild.name,
            inline=True
        )
        
        embed.add_field(
            name="🆔 ID",
            value=guild.id,
            inline=True
        )
        
        embed.add_field(
            name="👑 Dono",
            value=guild.owner.mention if guild.owner else "Desconhecido",
            inline=True
        )
        
        embed.add_field(
            name="⏰ Criado em",
            value=f"<t:{int(guild.created_at.timestamp())}:F>",
            inline=True
        )
        
        embed.add_field(
            name="🌍 Região",
            value=str(guild.region).replace('_', ' ').title() if hasattr(guild, 'region') else "Automática",
            inline=True
        )
        
        embed.add_field(
            name="📊 Nível de Verificação",
            value=str(guild.verification_level).replace('_', ' ').title(),
            inline=True
        )
        
        # Estatísticas
        total_members = guild.member_count
        online_members = len([m for m in guild.members if m.status != disnake.Status.offline])
        bot_count = len([m for m in guild.members if m.bot])
        
        embed.add_field(
            name="👥 Membros",
            value=f"**Total:** {total_members}\n**Online:** {online_members}\n**Bots:** {bot_count}",
            inline=True
        )
        
        # Canais
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        embed.add_field(
            name="📺 Canais",
            value=f"**Texto:** {text_channels}\n**Voz:** {voice_channels}\n**Categorias:** {categories}",
            inline=True
        )
        
        # Roles e emojis
        embed.add_field(
            name="🎭 Roles",
            value=len(guild.roles),
            inline=True
        )
        
        embed.add_field(
            name="😀 Emojis",
            value=f"{len(guild.emojis)}/{guild.emoji_limit}",
            inline=True
        )
        
        embed.add_field(
            name="🔗 Features",
            value=", ".join([f.replace('_', ' ').title() for f in guild.features]) if guild.features else "Nenhuma",
            inline=False
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.set_footer(text=f"ID: {guild.id}")
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="userinfo",
        description="Mostra informações de um usuário"
    )
    async def user_info(
        self,
        inter,
        user: disnake.Member = commands.Param(description="Usuário para ver informações", default=None)
    ):
        """Comando para mostrar informações de um usuário"""
        
        if user is None:
            user = inter.author
        
        embed = EmbedUtils.create_embed(
            title="👤 Informações do Usuário",
            description=f"Informações sobre **{user.display_name}**"
        )
        
        # Informações básicas
        embed.add_field(
            name="📝 Nome",
            value=user.name,
            inline=True
        )
        
        embed.add_field(
            name="🏷️ Nome de Exibição",
            value=user.display_name,
            inline=True
        )
        
        embed.add_field(
            name="🆔 ID",
            value=user.id,
            inline=True
        )
        
        embed.add_field(
            name="🤖 Bot",
            value="Sim" if user.bot else "Não",
            inline=True
        )
        
        embed.add_field(
            name="⏰ Conta Criada",
            value=f"<t:{int(user.created_at.timestamp())}:F>",
            inline=True
        )
        
        embed.add_field(
            name="📅 Entrou no Servidor",
            value=f"<t:{int(user.joined_at.timestamp())}:F>" if user.joined_at else "Desconhecido",
            inline=True
        )
        
        # Status
        status_emoji = {
            disnake.Status.online: "🟢",
            disnake.Status.idle: "🟡",
            disnake.Status.dnd: "🔴",
            disnake.Status.offline: "⚫"
        }
        
        embed.add_field(
            name="📊 Status",
            value=f"{status_emoji.get(user.status, '❓')} {str(user.status).title()}",
            inline=True
        )
        
        # Role principal
        embed.add_field(
            name="🎭 Role Principal",
            value=user.top_role.mention if user.top_role.name != "@everyone" else "Nenhuma",
            inline=True
        )
        
        embed.add_field(
            name="🎨 Cor",
            value=str(user.color),
            inline=True
        )
        
        # Roles
        roles = [role.mention for role in user.roles[1:]]  # Remove @everyone
        roles_text = ", ".join(roles) if roles else "Nenhuma"
        
        if len(roles_text) > 1024:
            roles_text = f"{len(roles)} roles"
        
        embed.add_field(
            name=f"🎭 Roles ({len(roles)})",
            value=roles_text,
            inline=False
        )
        
        # Atividade
        if user.activity:
            activity_text = f"**{user.activity.type.name.title()}:** {user.activity.name}"
            embed.add_field(
                name="🎮 Atividade",
                value=activity_text,
                inline=False
            )
        
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="avatar",
        description="Mostra o avatar de um usuário"
    )
    async def avatar(
        self,
        inter,
        user: disnake.Member = commands.Param(description="Usuário para ver o avatar", default=None)
    ):
        """Comando para mostrar o avatar de um usuário"""
        
        if user is None:
            user = inter.author
        
        embed = EmbedUtils.create_embed(
            title=f"🖼️ Avatar de {user.display_name}",
            description=f"Avatar de **{user.display_name}**"
        )
        
        embed.set_image(url=user.display_avatar.url)
        
        embed.add_field(
            name="🔗 Links",
            value=f"[PNG]({user.display_avatar.with_format('png').url}) • [JPG]({user.display_avatar.with_format('jpg').url}) • [WEBP]({user.display_avatar.with_format('webp').url})",
            inline=False
        )
        
        embed.set_footer(text=f"Solicitado por {inter.author.display_name}")
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="help",
        description="Mostra todos os comandos disponíveis"
    )
    async def help_command(self, inter):
        """Comando de ajuda personalizado"""
        
        embed = EmbedUtils.create_embed(
            title="📚 Central de Ajuda",
            description="Lista de todos os comandos disponíveis"
        )
        
        # Comandos de informação
        info_commands = [
            "`/ping` - Verifica latência e status",
            "`/uptime` - Tempo de atividade do bot",
            "`/status` - Informações do sistema",
            "`/info` - Informações do bot",
            "`/serverinfo` - Informações do servidor",
            "`/userinfo` - Informações de usuário",
            "`/avatar` - Avatar de usuário"
        ]
        
        embed.add_field(
            name="📊 Informações",
            value="\n".join(info_commands),
            inline=False
        )
        
        # Comandos de moderação
        mod_commands = [
            "`/kick` - Expulsar usuário",
            "`/ban` - Banir usuário",
            "`/unban` - Desbanir usuário",
            "`/timeout` - Colocar usuário em timeout",
            "`/clear` - Limpar mensagens",
            "`/warn` - Avisar usuário",
            "`/slowmode` - Controlar modo lento"
        ]
        
        embed.add_field(
            name="🔨 Moderação",
            value="\n".join(mod_commands),
            inline=False
        )
        
        # Comandos utilitários
        utility_commands = [
            "`/say` - Falar através do bot",
            "`/embed` - Criar embed personalizado",
            "`/poll` - Criar enquete",
            "`/remind` - Criar lembrete",
            "`/coinflip` - Cara ou coroa",
            "`/dice` - Rolar dados",
            "`/8ball` - Bola 8 mágica"
        ]
        
        embed.add_field(
            name="🛠️ Utilitários",
            value="\n".join(utility_commands),
            inline=False
        )
        
        embed.add_field(
            name="❓ Precisa de ajuda?",
            value="Entre em contato com a equipe de suporte do servidor!",
            inline=False
        )
        
        embed.set_footer(text="Use /help <comando> para mais informações sobre um comando específico")
        
        await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(InfoCog(bot))
