"""
Configurações do bot Discord
"""
import os
import disnake
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class BotConfig:
    """Classe para gerenciar configurações do bot"""
    
    # Token do bot
    TOKEN: str = os.getenv("TOKEN", "")
    
    # Configurações do bot
    COMMAND_PREFIX: str = "!"
    DESCRIPTION: str = "Bot Base - Um bot Discord moderno e otimizado"
    
    # Intents necessários
    INTENTS: disnake.Intents = disnake.Intents.default()
    INTENTS.guilds = True
    INTENTS.members = True
    INTENTS.message_content = True
    INTENTS.voice_states = True
    INTENTS.reactions = True
    
    # Configurações de embed padrão
    EMBED_COLOR: int = 0x5865F2  # Cor padrão do Discord
    SUCCESS_COLOR: int = 0x00FF00  # Verde
    ERROR_COLOR: int = 0xFF0000   # Vermelho
    WARNING_COLOR: int = 0xFFFF00  # Amarelo
    
    # Configurações de status
    STATUS_ACTIVITIES: list = [
        {"type": disnake.ActivityType.watching, "name": "por interações!"},
        {"type": disnake.ActivityType.listening, "name": "comandos /help"},
        {"type": disnake.ActivityType.playing, "name": "com Python e Disnake"}
    ]
    
    # Configurações de log
    LOG_CHANNEL: str = "bot-logs"
    LOG_LEVEL: str = "INFO"
    
    @classmethod
    def validate(cls) -> bool:
        """Valida se as configurações essenciais estão definidas"""
        if not cls.TOKEN:
            print("❌ TOKEN não foi definido no arquivo .env")
            return False
        return True
    
    @classmethod
    def get_embed_defaults(cls) -> Dict[str, Any]:
        """Retorna configurações padrão para embeds"""
        return {
            "color": cls.EMBED_COLOR,
            "timestamp": True
        }
