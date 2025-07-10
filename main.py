"""
Bot Discord Base - Moderno e Otimizado
Criado com Disnake e Python
"""

import disnake
import os
import asyncio
import logging
import random
from datetime import datetime
from disnake.ext import commands, tasks
from config import BotConfig
from utils import EmbedUtils, BotUtils

# Configurar logging
logger = logging.getLogger(__name__)

class BotBase(commands.InteractionBot):
    """Classe principal do bot com funcionalidades otimizadas"""
    
    def __init__(self):
        super().__init__(
            intents=BotConfig.INTENTS,
            command_prefix=BotConfig.COMMAND_PREFIX,
            description=BotConfig.DESCRIPTION,
            help_command=None,
            sync_commands=True
        )
        
        # Atributos do bot
        self.start_time = datetime.utcnow()
        self.config = BotConfig
        
        # Carregar extensões
        self.load_extensions()
        
        # Iniciar tasks
        self.status_task.start()
    
    def load_extensions(self):
        """Carrega todas as extensões (cogs)"""
        initial_extensions = [
            'cogs.ping_cog',
            'cogs.info_cog',
            'cogs.moderation_cog',
            'cogs.utility_cog'
        ]
        
        loaded_extensions = []
        failed_extensions = []
        
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
                loaded_extensions.append(extension)
                logger.info(f"✅ Extensão carregada: {extension}")
            except Exception as e:
                failed_extensions.append(extension)
                logger.error(f"❌ Falha ao carregar extensão {extension}: {e}")
        
        print(f"\n🔧 Extensões carregadas: {len(loaded_extensions)}")
        for ext in loaded_extensions:
            print(f"  ✅ {ext}")
        
        if failed_extensions:
            print(f"\n❌ Extensões que falharam: {len(failed_extensions)}")
            for ext in failed_extensions:
                print(f"  ❌ {ext}")
    
    @tasks.loop(minutes=5)
    async def status_task(self):
        """Alterna o status do bot"""
        if not self.is_ready():
            return
        
        activity_config = random.choice(BotConfig.STATUS_ACTIVITIES)
        activity = disnake.Activity(
            type=activity_config["type"],
            name=activity_config["name"]
        )
        await self.change_presence(activity=activity)
    
    @status_task.before_loop
    async def before_status_task(self):
        """Espera o bot estar pronto antes de iniciar a task"""
        await self.wait_until_ready()
    
    async def on_ready(self):
        """Evento executado quando o bot está pronto"""
        print("=" * 50)
        print(f"🤖 Bot conectado com sucesso!")
        print(f"📝 Nome: {self.user.name}")
        print(f"🆔 ID: {self.user.id}")
        print(f"🌐 Servidores: {len(self.guilds)}")
        print(f"👥 Usuários: {len(self.users)}")
        print(f"📊 Latência: {round(self.latency * 1000)}ms")
        print(f"🐍 Versão do Disnake: {disnake.__version__}")
        print(f"⏰ Iniciado em: {self.start_time.strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 50)
        
        # Definir status inicial
        activity = disnake.Activity(
            type=disnake.ActivityType.watching,
            name="por interações!"
        )
        await self.change_presence(activity=activity)
        
        logger.info(f"Bot {self.user.name} está online!")
    
    async def on_guild_join(self, guild):
        """Evento executado quando o bot entra em um servidor"""
        logger.info(f"Bot adicionado ao servidor: {guild.name} (ID: {guild.id})")
        
        # Enviar mensagem de boas-vindas para o canal geral
        if guild.system_channel:
            embed = EmbedUtils.create_embed(
                title="Obrigado por me adicionar!",
                description=(
                    f"Olá pessoal do **{guild.name}**! 👋\n\n"
                    "Eu sou um bot moderno feito com Python e Disnake.\n"
                    "Use `/help` para ver todos os meus comandos!\n\n"
                    "📝 **Comandos principais:**\n"
                    "`/ping` - Verificar latência\n"
                    "`/ticket` - Sistema de tickets\n"
                    "`/info` - Informações do bot\n"
                ),
                color=BotConfig.SUCCESS_COLOR
            )
            
            try:
                await guild.system_channel.send(embed=embed)
            except:
                pass
    
    async def on_guild_remove(self, guild):
        """Evento executado quando o bot sai de um servidor"""
        logger.info(f"Bot removido do servidor: {guild.name} (ID: {guild.id})")
    
    async def on_application_command_error(self, inter, error):
        """Trata erros de comandos slash"""
        if isinstance(error, commands.CommandOnCooldown):
            embed = EmbedUtils.error_embed(
                title="Comando em cooldown",
                description=f"Tente novamente em {error.retry_after:.1f} segundos."
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
        
        elif isinstance(error, commands.MissingPermissions):
            embed = EmbedUtils.error_embed(
                title="Permissões insuficientes",
                description="Você não tem permissão para usar este comando."
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
        
        elif isinstance(error, commands.BotMissingPermissions):
            embed = EmbedUtils.error_embed(
                title="Bot sem permissões",
                description="Eu não tenho as permissões necessárias para executar este comando."
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
        
        else:
            logger.error(f"Erro não tratado: {error}")
            embed = EmbedUtils.error_embed(
                title="Erro inesperado",
                description="Ocorreu um erro inesperado. Tente novamente."
            )
            
            try:
                await inter.response.send_message(embed=embed, ephemeral=True)
            except:
                pass
    
    def get_uptime(self):
        """Retorna o tempo de atividade do bot"""
        delta = datetime.utcnow() - self.start_time
        return BotUtils.format_uptime(int(delta.total_seconds()))

# Inicializar o bot
def main():
    """Função principal"""
    # Validar configurações
    if not BotConfig.validate():
        print("❌ Configurações inválidas! Verifique o arquivo .env")
        return
    
    # Criar instância do bot
    bot = BotBase()
    
    # Executar o bot
    try:
        bot.run(BotConfig.TOKEN)
    except disnake.LoginFailure:
        logger.error("❌ Token inválido!")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar o bot: {e}")

if __name__ == "__main__":
    main()