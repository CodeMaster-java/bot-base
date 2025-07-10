@echo off
title Setup - Bot Base
echo.
echo ===============================================
echo           Setup - Bot Base
echo ===============================================
echo.
echo [INFO] Configurando o bot base...
echo.

echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado!
    echo [INFO] Baixe e instale o Python em: https://python.org
    pause
    exit /b 1
)
echo [OK] Python encontrado!

echo.
echo [2/4] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias!
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas!

echo.
echo [3/4] Configurando arquivos...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo [OK] Arquivo .env criado!
    ) else (
        echo [ERRO] Arquivo .env.example nao encontrado!
        pause
        exit /b 1
    )
) else (
    echo [OK] Arquivo .env ja existe!
)

echo.
echo [4/4] Criando diretorios...
if not exist "logs" mkdir logs
echo [OK] Diretorio de logs criado!

echo.
echo ===============================================
echo           Setup Concluido!
echo ===============================================
echo.
echo [IMPORTANTE] Agora voce precisa:
echo 1. Editar o arquivo .env
echo 2. Adicionar o token do seu bot
echo 3. Executar start.bat para iniciar o bot
echo.
echo [INFO] Para obter um token:
echo 1. Acesse https://discord.com/developers/applications
echo 2. Crie uma nova aplicacao
echo 3. Va para a aba "Bot"
echo 4. Clique em "Reset Token" e copie o token
echo 5. Cole o token no arquivo .env
echo.
pause
