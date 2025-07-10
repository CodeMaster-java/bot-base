"""
Utilitários para o bot Discord
"""
import disnake
import asyncio
import logging
from typing import Optional, Union, List
from datetime import datetime
from config import BotConfig

# Configurar logging
logging.basicConfig(
    level=getattr(logging, BotConfig.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

class EmbedUtils:
    """Utilitários para criar embeds padronizados"""
    
    @staticmethod
    def create_embed(
        title: str = None,
        description: str = None,
        color: int = BotConfig.EMBED_COLOR,
        author: disnake.Member = None,
        footer: str = None,
        thumbnail: str = None,
        image: str = None,
        timestamp: bool = True
    ) -> disnake.Embed:
        """Cria um embed com configurações padrão"""
        embed = disnake.Embed(
            title=title,
            description=description,
            color=color
        )
        
        if timestamp:
            embed.timestamp = datetime.utcnow()
        
        if author:
            embed.set_author(
                name=author.display_name,
                icon_url=author.display_avatar.url
            )
        
        if footer:
            embed.set_footer(text=footer)
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        
        if image:
            embed.set_image(url=image)
        
        return embed
    
    @staticmethod
    def success_embed(title: str = "Sucesso", description: str = None) -> disnake.Embed:
        """Cria um embed de sucesso"""
        return EmbedUtils.create_embed(
            title=f"✅ {title}",
            description=description,
            color=BotConfig.SUCCESS_COLOR
        )
    
    @staticmethod
    def error_embed(title: str = "Erro", description: str = None) -> disnake.Embed:
        """Cria um embed de erro"""
        return EmbedUtils.create_embed(
            title=f"❌ {title}",
            description=description,
            color=BotConfig.ERROR_COLOR
        )
    
    @staticmethod
    def warning_embed(title: str = "Aviso", description: str = None) -> disnake.Embed:
        """Cria um embed de aviso"""
        return EmbedUtils.create_embed(
            title=f"⚠️ {title}",
            description=description,
            color=BotConfig.WARNING_COLOR
        )

class BotUtils:
    """Utilitários gerais para o bot"""
    
    @staticmethod
    def format_uptime(seconds: int) -> str:
        """Formata tempo de atividade"""
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0:
            parts.append(f"{seconds}s")
        
        return " ".join(parts) if parts else "0s"
    
    @staticmethod
    def get_member_permissions(member: disnake.Member) -> List[str]:
        """Retorna uma lista de permissões do membro"""
        perms = []
        for perm, value in member.guild_permissions:
            if value:
                perms.append(perm.replace('_', ' ').title())
        return perms
    
    @staticmethod
    async def safe_delete_message(message: disnake.Message, delay: int = 0) -> bool:
        """Deleta uma mensagem com segurança"""
        try:
            if delay > 0:
                await asyncio.sleep(delay)
            await message.delete()
            return True
        except:
            return False
    
    @staticmethod
    def get_user_info(user: Union[disnake.User, disnake.Member]) -> dict:
        """Retorna informações formatadas do usuário"""
        info = {
            "id": user.id,
            "name": user.name,
            "display_name": user.display_name,
            "avatar": user.display_avatar.url,
            "created_at": user.created_at,
            "bot": user.bot
        }
        
        if isinstance(user, disnake.Member):
            info.update({
                "joined_at": user.joined_at,
                "roles": [role.name for role in user.roles[1:]],  # Remove @everyone
                "top_role": user.top_role.name,
                "permissions": BotUtils.get_member_permissions(user)
            })
        
        return info

class DatabaseUtils:
    """Utilitários para banco de dados (placeholder para futuras implementações)"""
    
    @staticmethod
    async def setup_database():
        """Configura o banco de dados"""
        # Implementar quando necessário
        pass
    
    @staticmethod
    async def close_database():
        """Fecha conexão com banco de dados"""
        # Implementar quando necessário
        pass
