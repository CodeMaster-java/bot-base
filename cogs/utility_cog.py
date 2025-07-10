"""
Cog de comandos utilitários
"""

import disnake
import asyncio
import random
from datetime import datetime, timedelta
from disnake.ext import commands, tasks
from utils import EmbedUtils, BotUtils
from config import BotConfig

class PollView(disnake.ui.View):
    """View para enquetes"""
    
    def __init__(self, options):
        super().__init__(timeout=300)  # 5 minutos
        self.options = options
        self.votes = {i: [] for i in range(len(options))}
        
        # Criar botões dinamicamente
        for i, option in enumerate(options):
            button = disnake.ui.Button(
                label=f"{i+1}. {option}",
                style=disnake.ButtonStyle.primary,
                custom_id=f"poll_{i}"
            )
            button.callback = self.create_vote_callback(i)
            self.add_item(button)
    
    def create_vote_callback(self, option_index):
        async def vote_callback(inter):
            user_id = inter.user.id
            
            # Remover voto anterior se existir
            for votes_list in self.votes.values():
                if user_id in votes_list:
                    votes_list.remove(user_id)
            
            # Adicionar novo voto
            self.votes[option_index].append(user_id)
            
            # Atualizar embed
            embed = EmbedUtils.create_embed(
                title="📊 Enquete",
                description="Clique em uma opção para votar!"
            )
            
            total_votes = sum(len(votes) for votes in self.votes.values())
            
            for i, option in enumerate(self.options):
                vote_count = len(self.votes[i])
                percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
                
                # Criar barra de progresso
                bar_length = 10
                filled_length = int(bar_length * percentage / 100)
                bar = "█" * filled_length + "░" * (bar_length - filled_length)
                
                embed.add_field(
                    name=f"{i+1}. {option}",
                    value=f"`{bar}` {vote_count} votos ({percentage:.1f}%)",
                    inline=False
                )
            
            embed.set_footer(text=f"Total de votos: {total_votes}")
            
            await inter.response.edit_message(embed=embed, view=self)
        
        return vote_callback

class ReminderModal(disnake.ui.Modal):
    """Modal para criar lembretes"""
    
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Tempo (ex: 1h, 30m, 2d)",
                placeholder="Ex: 1h30m, 2d, 45m...",
                custom_id="time_input",
                max_length=50
            ),
            disnake.ui.TextInput(
                label="Lembrete",
                placeholder="Do que você quer ser lembrado?",
                custom_id="reminder_input",
                style=disnake.TextInputStyle.paragraph,
                max_length=1000
            )
        ]
        super().__init__(title="Criar Lembrete", components=components)
    
    async def callback(self, inter: disnake.ModalInteraction):
        time_str = inter.text_values["time_input"]
        reminder_text = inter.text_values["reminder_input"]
        
        # Converter tempo para segundos
        seconds = self.parse_time(time_str)
        
        if seconds is None:
            embed = EmbedUtils.error_embed(
                title="Formato inválido",
                description="Use formatos como: 1h, 30m, 2d, 1h30m, etc."
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        if seconds > 604800:  # 7 dias
            embed = EmbedUtils.error_embed(
                title="Tempo muito longo",
                description="O tempo máximo é de 7 dias!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Criar lembrete
        reminder_time = datetime.utcnow() + timedelta(seconds=seconds)
        
        embed = EmbedUtils.success_embed(
            title="Lembrete criado",
            description=f"Você será lembrado em **{time_str}**"
        )
        embed.add_field(name="Lembrete", value=reminder_text, inline=False)
        embed.add_field(name="Quando", value=f"<t:{int(reminder_time.timestamp())}:F>", inline=False)
        
        await inter.response.send_message(embed=embed, ephemeral=True)
        
        # Aguardar e enviar lembrete
        await asyncio.sleep(seconds)
        
        reminder_embed = EmbedUtils.create_embed(
            title="🔔 Lembrete",
            description=reminder_text,
            color=BotConfig.WARNING_COLOR
        )
        reminder_embed.add_field(
            name="Criado em",
            value=f"<t:{int((reminder_time - timedelta(seconds=seconds)).timestamp())}:F>",
            inline=False
        )
        
        try:
            await inter.user.send(embed=reminder_embed)
        except:
            # Se não conseguir enviar DM, tentar no canal
            try:
                await inter.channel.send(f"{inter.user.mention}", embed=reminder_embed)
            except:
                pass
    
    def parse_time(self, time_str):
        """Converte string de tempo para segundos"""
        import re
        
        # Padrões de tempo
        patterns = {
            'd': 86400,  # dias
            'h': 3600,   # horas
            'm': 60,     # minutos
            's': 1       # segundos
        }
        
        total_seconds = 0
        time_str = time_str.lower().strip()
        
        for unit, multiplier in patterns.items():
            match = re.search(rf'(\d+){unit}', time_str)
            if match:
                total_seconds += int(match.group(1)) * multiplier
        
        return total_seconds if total_seconds > 0 else None

class UtilityCog(commands.Cog):
    """Comandos utilitários diversos"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="say",
        description="Faz o bot falar algo"
    )
    @commands.has_permissions(manage_messages=True)
    async def say(
        self,
        inter,
        message: str = commands.Param(description="Mensagem para o bot falar"),
        channel: disnake.TextChannel = commands.Param(description="Canal para enviar (opcional)", default=None)
    ):
        """Comando para fazer o bot falar"""
        
        target_channel = channel or inter.channel
        
        try:
            await target_channel.send(message)
            
            if channel:
                embed = EmbedUtils.success_embed(
                    title="Mensagem enviada",
                    description=f"Mensagem enviada para {target_channel.mention}"
                )
                await inter.response.send_message(embed=embed, ephemeral=True)
            else:
                await inter.response.send_message("✅ Mensagem enviada!", ephemeral=True)
                
        except disnake.Forbidden:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Não tenho permissão para enviar mensagens neste canal!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
    
    @commands.slash_command(
        name="embed",
        description="Cria um embed personalizado"
    )
    @commands.has_permissions(manage_messages=True)
    async def create_embed(
        self,
        inter,
        title: str = commands.Param(description="Título do embed"),
        description: str = commands.Param(description="Descrição do embed"),
        color: str = commands.Param(description="Cor do embed (hex, ex: #FF0000)", default=None),
        image: str = commands.Param(description="URL da imagem", default=None),
        thumbnail: str = commands.Param(description="URL da thumbnail", default=None),
        footer: str = commands.Param(description="Texto do rodapé", default=None)
    ):
        """Comando para criar embeds personalizados"""
        
        # Processar cor
        embed_color = BotConfig.EMBED_COLOR
        if color:
            try:
                if color.startswith('#'):
                    embed_color = int(color[1:], 16)
                else:
                    embed_color = int(color, 16)
            except ValueError:
                embed_color = BotConfig.EMBED_COLOR
        
        # Criar embed
        embed = disnake.Embed(
            title=title,
            description=description,
            color=embed_color,
            timestamp=datetime.utcnow()
        )
        
        if image:
            embed.set_image(url=image)
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        
        if footer:
            embed.set_footer(text=footer)
        else:
            embed.set_footer(text=f"Criado por {inter.author.display_name}")
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="poll",
        description="Cria uma enquete"
    )
    async def poll(
        self,
        inter,
        question: str = commands.Param(description="Pergunta da enquete"),
        option1: str = commands.Param(description="Primeira opção"),
        option2: str = commands.Param(description="Segunda opção"),
        option3: str = commands.Param(description="Terceira opção", default=None),
        option4: str = commands.Param(description="Quarta opção", default=None),
        option5: str = commands.Param(description="Quinta opção", default=None)
    ):
        """Comando para criar enquetes"""
        
        # Coletar opções
        options = [option1, option2]
        for opt in [option3, option4, option5]:
            if opt:
                options.append(opt)
        
        # Criar embed
        embed = EmbedUtils.create_embed(
            title="📊 Enquete",
            description=f"**{question}**\n\nClique em uma opção para votar!"
        )
        
        # Adicionar opções
        for i, option in enumerate(options):
            embed.add_field(
                name=f"{i+1}. {option}",
                value="`░░░░░░░░░░` 0 votos (0.0%)",
                inline=False
            )
        
        embed.set_footer(text=f"Enquete criada por {inter.author.display_name} • Total de votos: 0")
        
        # Criar view
        view = PollView(options)
        
        await inter.response.send_message(embed=embed, view=view)
    
    @commands.slash_command(
        name="remind",
        description="Cria um lembrete"
    )
    async def remind(self, inter):
        """Comando para criar lembretes"""
        
        modal = ReminderModal()
        await inter.response.send_modal(modal)
    
    @commands.slash_command(
        name="coinflip",
        description="Joga uma moeda"
    )
    async def coinflip(self, inter):
        """Comando para jogar moeda"""
        
        result = random.choice(["Cara", "Coroa"])
        emoji = "🪙" if result == "Cara" else "🔘"
        
        embed = EmbedUtils.create_embed(
            title="🪙 Cara ou Coroa",
            description=f"{emoji} **{result}**!"
        )
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="dice",
        description="Rola um dado"
    )
    async def dice(
        self,
        inter,
        sides: int = commands.Param(description="Número de lados do dado", default=6, min_value=2, max_value=100)
    ):
        """Comando para rolar dados"""
        
        result = random.randint(1, sides)
        
        embed = EmbedUtils.create_embed(
            title="🎲 Dados",
            description=f"Você rolou um **{result}** em um dado de {sides} lados!"
        )
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="choose",
        description="Escolhe uma opção aleatória"
    )
    async def choose(
        self,
        inter,
        options: str = commands.Param(description="Opções separadas por vírgula")
    ):
        """Comando para escolher entre opções"""
        
        choices = [choice.strip() for choice in options.split(',')]
        
        if len(choices) < 2:
            embed = EmbedUtils.error_embed(
                title="Erro",
                description="Você precisa fornecer pelo menos 2 opções separadas por vírgula!"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        chosen = random.choice(choices)
        
        embed = EmbedUtils.create_embed(
            title="🎯 Escolha Aleatória",
            description=f"Eu escolho: **{chosen}**"
        )
        
        embed.add_field(
            name="Opções",
            value="\n".join([f"• {choice}" for choice in choices]),
            inline=False
        )
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="8ball",
        description="Pergunta para a bola 8"
    )
    async def eight_ball(
        self,
        inter,
        question: str = commands.Param(description="Sua pergunta")
    ):
        """Comando da bola 8"""
        
        responses = [
            "🟢 Sim, definitivamente",
            "🟢 É certo",
            "🟢 Sem dúvida",
            "🟢 Sim",
            "🟢 Você pode contar com isso",
            "🟢 Como eu vejo, sim",
            "🟢 Muito provável",
            "🟢 Perspectiva boa",
            "🟡 Resposta nebulosa, tente novamente",
            "🟡 Pergunte novamente mais tarde",
            "🟡 Melhor não te dizer agora",
            "🟡 Não é possível prever agora",
            "🟡 Concentre-se e pergunte novamente",
            "🔴 Não conte com isso",
            "🔴 Minha resposta é não",
            "🔴 Minhas fontes dizem que não",
            "🔴 Perspectiva não muito boa",
            "🔴 Muito duvidoso"
        ]
        
        response = random.choice(responses)
        
        embed = EmbedUtils.create_embed(
            title="🎱 Bola 8",
            description=f"**Pergunta:** {question}\n\n**Resposta:** {response}"
        )
        
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command(
        name="afk",
        description="Define seu status como AFK"
    )
    async def afk(
        self,
        inter,
        reason: str = commands.Param(description="Motivo do AFK", default="AFK")
    ):
        """Comando para definir status AFK"""
        
        # Aqui você pode implementar um sistema de AFK com banco de dados
        # Por enquanto, apenas uma mensagem
        
        embed = EmbedUtils.success_embed(
            title="AFK Ativado",
            description=f"Você está AFK: **{reason}**"
        )
        
        await inter.response.send_message(embed=embed, ephemeral=True)
    
    @commands.slash_command(
        name="shorturl",
        description="Encurta uma URL"
    )
    async def shorten_url(
        self,
        inter,
        url: str = commands.Param(description="URL para encurtar")
    ):
        """Comando para encurtar URLs"""
        
        # Validação básica de URL
        if not url.startswith(('http://', 'https://')):
            embed = EmbedUtils.error_embed(
                title="URL inválida",
                description="A URL deve começar com http:// ou https://"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Aqui você pode implementar um serviço de encurtamento
        # Por enquanto, apenas uma resposta de exemplo
        
        embed = EmbedUtils.create_embed(
            title="🔗 URL Encurtada",
            description="Serviço de encurtamento ainda não implementado"
        )
        
        embed.add_field(name="URL Original", value=url, inline=False)
        embed.add_field(name="Status", value="Em desenvolvimento", inline=False)
        
        await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(UtilityCog(bot))
