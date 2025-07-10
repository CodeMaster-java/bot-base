@echo off
title Bot Base - Discord Bot
echo.
echo ===============================================
echo            Bot Base - Discord Bot
echo ===============================================
echo.
echo [INFO] Verificando instalacao do Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado!
    echo [INFO] Baixe e instale o Python em: https://python.org
    pause
    exit /b 1
)

echo [INFO] Python encontrado!
echo.

echo [INFO] Verificando dependencias...
if not exist "requirements.txt" (
    echo [ERRO] Arquivo requirements.txt nao encontrado!
    pause
    exit /b 1
)

echo [INFO] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo [INFO] Dependencias instaladas com sucesso!
echo.

echo [INFO] Verificando configuracao...
if not exist ".env" (
    echo [AVISO] Arquivo .env nao encontrado!
    echo [INFO] Copiando arquivo de exemplo...
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo [INFO] Arquivo .env criado a partir do exemplo.
        echo [IMPORTANTE] Edite o arquivo .env e adicione seu token!
        echo.
        pause
    ) else (
        echo [ERRO] Arquivo .env.example nao encontrado!
        pause
        exit /b 1
    )
)

echo [INFO] Iniciando o bot...
echo.
python main.py
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] O bot encerrou com erro!
    echo [INFO] Verifique o arquivo .env e seu token.
)

echo.
echo [INFO] Bot encerrado.
pause
