# 🤖 Bot Base - Discord Bot Moderno

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Disnake](https://img.shields.io/badge/Disnake-2.9%2B-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen.svg)

Um bot Discord moderno e otimizado feito com Python e Disnake, perfeito como base para seus projetos!

## ✨ Características

- 🚀 **Moderno**: Construído com as mais recentes versões do Python e Disnake
- 🎛️ **Slash Commands**: Suporte completo a comandos de barra
- 🔧 **Configurável**: Configurações centralizadas e facilmente customizáveis
- 📊 **Informativo**: Comandos ricos com embeds coloridos e informativos
- 🛡️ **Seguro**: Sistema de verificações e tratamento de erros
- 📝 **Bem Documentado**: Código limpo e bem comentado
- 🎨 **Interface Rica**: Embeds bonitos e interações intuitivas
- 🎮 **Interativo**: Jogos e utilitários divertidos

## 🎯 Funcionalidades

### 📊 Comandos de Informação
- `/ping` - Latência e informações do bot
- `/uptime` - Tempo de atividade
- `/status` - Informações detalhadas do sistema
- `/info` - Informações completas do bot
- `/serverinfo` - Informações do servidor
- `/userinfo` - Informações de usuário
- `/avatar` - Visualizar avatar de usuário
- `/help` - Central de ajuda completa

### 🔨 Moderação
- `/kick` - Expulsar usuário
- `/ban` - Banir usuário
- `/unban` - Desbanir usuário
- `/timeout` - Timeout de usuário
- `/untimeout` - Remover timeout
- `/clear` - Limpar mensagens
- `/warn` - Avisar usuário
- `/slowmode` - Controlar modo lento

### 🛠️ Utilitários
- `/say` - Fazer o bot falar
- `/embed` - Criar embeds personalizados
- `/poll` - Criar enquetes interativas
- `/remind` - Sistema de lembretes
- `/coinflip` - Cara ou coroa
- `/dice` - Rolar dados
- `/choose` - Escolher entre opções
- `/8ball` - Bola 8 mágica
- `/afk` - Status AFK

## 🚀 Instalação

### 1. Pré-requisitos
- Python 3.8 ou superior
- Git (opcional)

### 2. Clonando o repositório
```bash
git clone https://github.com/CodeMaster-java/bot-base.git
cd bot-base
```

### 3. Instalando dependências
```bash
pip install -r requirements.txt
```

### 4. Configuração
1. Renomeie `.env.example` para `.env` (se existir) ou edite o arquivo `.env`
2. Adicione o token do seu bot:
```env
TOKEN=SEU_TOKEN_AQUI
```

### 5. Executando o bot
```bash
python main.py
```

## ⚙️ Configuração

### Arquivo .env
```env
# Token do bot Discord
TOKEN=seu_token_aqui

# Configurações opcionais
PREFIX=!
EMBED_COLOR=5865F2

# Configurações de logs
LOG_LEVEL=INFO
LOG_CHANNEL=bot-logs

# Configurações de desenvolvimento
DEBUG=False
DEVELOPMENT_MODE=False
```

### Arquivo config.py
O arquivo `config.py` contém todas as configurações centralizadas do bot:
- Cores dos embeds
- Atividades do bot
- Configurações de intents
- Validações automáticas

## 📁 Estrutura do Projeto

```
bot-base/
│
├── main.py                 # Arquivo principal do bot
├── config.py               # Configurações centralizadas
├── utils.py                # Utilitários e funções auxiliares
├── requirements.txt        # Dependências do projeto
├── .env                    # Variáveis de ambiente
├── README.md              # Este arquivo
│
├── cogs/                  # Comandos organizados em cogs
│   ├── ping_cog.py        # Comandos de ping e status
│   ├── info_cog.py        # Comandos de informação
│   ├── moderation_cog.py  # Comandos de moderação
│   └── utility_cog.py     # Comandos utilitários
│
└── logs/                  # Logs do bot (criado automaticamente)
    └── bot.log
```

## 🔧 Personalização

### Adicionando novos comandos
1. Crie um novo arquivo na pasta `cogs/`
2. Siga o padrão dos cogs existentes
3. Adicione o nome do cog em `main.py` na lista `initial_extensions`

### Customizando embeds
Edite o arquivo `utils.py` para personalizar:
- Cores padrão
- Formatos de embed
- Utilitários diversos

### Configurando o bot
Edite o arquivo `config.py` para:
- Alterar atividades do bot
- Modificar cores
- Configurar intents
- Definir configurações padrão

## 🎨 Capturas de Tela

### Comando /ping
![Ping Command](https://via.placeholder.com/600x300?text=Comando+Ping)

### Comando /help
![Help Command](https://via.placeholder.com/600x300?text=Comando+Help)

### Comandos de Moderação
![Moderation Commands](https://via.placeholder.com/600x300?text=Comandos+de+Moderação)

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🐛 Reportando Bugs

Se você encontrar um bug:

1. Verifique se já não foi reportado nas [Issues](https://github.com/seu-usuario/bot-base/issues)
2. Crie uma nova issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Screenshots (se aplicável)

## 📝 Changelog

### v2.0.0 (2025-01-10)
- 🚀 Reestruturação completa do código
- 🎨 Interface renovada com embeds ricos
- 🔧 Sistema de configuração centralizada
- 📊 Comandos de informação melhorados
- 🛡️ Sistema de moderação completo
- 🎯 Utilitários diversos adicionados
- 🎮 Jogos e entretenimento
- 📝 Documentação completa

### v1.0.0 (2023-01-01)
- 🎉 Versão inicial
- ⚡ Comandos básicos de ping e ticket

## 🆘 Suporte

Se precisar de ajuda:

- 📧 Email: suporte@exemplo.com
- 💬 Discord: [Servidor de Suporte](https://discord.gg/exemplo)
- 📖 Wiki: [Wiki do Projeto](https://github.com/seu-usuario/bot-base/wiki)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- [Disnake](https://github.com/DisnakeDev/disnake) - A biblioteca que tornou tudo possível
- [Discord.py](https://github.com/Rapptz/discord.py) - Inspiração para muitas implementações
- Comunidade Python - Pelo apoio e recursos

## 📚 Recursos Úteis

- [Documentação do Disnake](https://docs.disnake.dev/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Python.org](https://www.python.org/)
- [Guia de Markdown](https://guides.github.com/features/mastering-markdown/)

---

<div align="center">
  <p>Feito com ❤️ por <a href="https://github.com/CodeMaster-java">Code Master</a></p>
  <p>⭐ Não se esqueça de dar uma star se este projeto te ajudou!</p>
</div>
