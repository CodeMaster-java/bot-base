"""
Cog de comandos de ping e informações básicas
"""

import disnake
import psutil
import platform
from datetime import datetime
from disnake.ext import commands
from utils import EmbedUtils, BotUtils

class PingCog(commands.Cog):
    """Comandos relacionados a ping e informações do bot"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name='ping',
        description='Verifica a latência do bot e informações de conexão'
    )
    async def ping(self, inter):
        """Comando para verificar latência e status do bot"""
        
        # Calcular latência
        latency_ms = round(self.bot.latency * 1000)
        
        # Obter informações do sistema
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_usage = f"{memory.percent}%"
        
        # Criar embed com informações detalhadas
        embed = EmbedUtils.create_embed(
            title="🏓 Pong!",
            description="Informações de latência e status do bot",
            color=0x00ff00 if latency_ms < 100 else 0xffff00 if latency_ms < 200 else 0xff0000
        )
        
        # Adicionar campos
        embed.add_field(
            name="📡 Latência",
            value=f"`{latency_ms}ms`",
            inline=True
        )
        
        embed.add_field(
            name="⏱️ Uptime",
            value=f"`{self.bot.get_uptime()}`",
            inline=True
        )
        
        embed.add_field(
            name="🖥️ CPU",
            value=f"`{cpu_usage}%`",
            inline=True
        )
        
        embed.add_field(
            name="💾 RAM",
            value=f"`{memory_usage}`",
            inline=True
        )
        
        embed.add_field(
            name="🌐 Servidores",
            value=f"`{len(self.bot.guilds)}`",
            inline=True
        )
        
        embed.add_field(
            name="👥 Usuários",
            value=f"`{len(self.bot.users)}`",
            inline=True
        )
        
        # Status de conexão
        status_emoji = "🟢" if latency_ms < 100 else "🟡" if latency_ms < 200 else "🔴"
        status_text = "Excelente" if latency_ms < 100 else "Boa" if latency_ms < 200 else "Ruim"
        
        embed.add_field(
            name="📊 Status da Conexão",
            value=f"{status_emoji} {status_text}",
            inline=False
        )
        
        # Adicionar timestamp
        embed.set_footer(text=f"Solicitado por {inter.author.display_name}")
        
        await inter.response.send_message(embed=embed, ephemeral=True)
    
    @commands.slash_command(
        name='uptime',
        description='Mostra há quanto tempo o bot está online'
    )
    async def uptime(self, inter):
        """Comando para mostrar o tempo de atividade do bot"""
        
        uptime_str = self.bot.get_uptime()
        start_time = self.bot.start_time.strftime('%d/%m/%Y às %H:%M:%S')
        
        embed = EmbedUtils.create_embed(
            title="⏰ Tempo de Atividade",
            description=f"O bot está online há **{uptime_str}**",
            color=0x00ff00
        )
        
        embed.add_field(
            name="🚀 Iniciado em",
            value=start_time,
            inline=False
        )
        
        embed.add_field(
            name="📈 Estatísticas",
            value=(
                f"**Servidores:** {len(self.bot.guilds)}\n"
                f"**Usuários:** {len(self.bot.users)}\n"
                f"**Comandos:** {len(self.bot.slash_commands)}"
            ),
            inline=False
        )
        
        await inter.response.send_message(embed=embed, ephemeral=True)
    
    @commands.slash_command(
        name='status',
        description='Mostra informações detalhadas do sistema'
    )
    async def status(self, inter):
        """Comando para mostrar status detalhado do sistema"""
        
        # Informações do sistema
        system_info = {
            "OS": platform.system(),
            "Version": platform.release(),
            "Architecture": platform.machine(),
            "Python": platform.python_version(),
            "Disnake": disnake.__version__
        }
        
        # Informações de hardware
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        embed = EmbedUtils.create_embed(
            title="📊 Status do Sistema",
            description="Informações detalhadas do bot e sistema"
        )
        
        # Sistema
        system_text = "\n".join([f"**{key}:** {value}" for key, value in system_info.items()])
        embed.add_field(
            name="🖥️ Sistema",
            value=system_text,
            inline=False
        )
        
        # Hardware
        hardware_text = (
            f"**CPU Cores:** {cpu_count}\n"
            f"**RAM Total:** {memory.total // (1024**3)} GB\n"
            f"**RAM Usada:** {memory.used // (1024**3)} GB ({memory.percent}%)\n"
            f"**Disco Usado:** {disk.used // (1024**3)} GB ({disk.percent}%)"
        )
        embed.add_field(
            name="⚙️ Hardware",
            value=hardware_text,
            inline=False
        )
        
        # Bot
        bot_text = (
            f"**Latência:** {round(self.bot.latency * 1000)}ms\n"
            f"**Uptime:** {self.bot.get_uptime()}\n"
            f"**Servidores:** {len(self.bot.guilds)}\n"
            f"**Usuários:** {len(self.bot.users)}"
        )
        embed.add_field(
            name="🤖 Bot",
            value=bot_text,
            inline=False
        )
        
        await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(PingCog(bot))
