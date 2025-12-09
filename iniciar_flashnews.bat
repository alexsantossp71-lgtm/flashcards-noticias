@echo off
title Launcher FlashNews AI
color 0A

echo ==========================================
echo       INICIANDO FLASHNEWS AI
echo ==========================================
echo.

:: 0. Parar servicos anteriores
echo [0/4] Parando servicos antigos...
taskkill /F /FI "WINDOWTITLE eq FlashNews Server*" /T 2>NUL
taskkill /F /IM "ollama.exe" /T 2>NUL
timeout /t 2 >nul
echo    -> Servicos parados. Limpeza concluida.
echo.

:: 1. Iniciar Ollama
echo [1/4] Iniciando servico de IA (Ollama)...
set "OLLAMA_PATH=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"

if exist "%OLLAMA_PATH%" (
    start "Ollama" /MIN "%OLLAMA_PATH%" serve
    echo    -> Ollama iniciado.
) else (
    start "Ollama" /MIN ollama serve
    echo    -> Ollama iniciado pelo PATH.
)
echo.

:: 2. Iniciar Servidor Backend
echo [2/4] Iniciando Servidor Backend (Python + Ollama)...
if exist "venv312\Scripts\python.exe" (
    start "FlashNews Server" /MIN cmd /k "cd /d %~dp0 && venv312\Scripts\activate && cd backend && python server.py"
    echo    -> Servidor iniciado em segundo plano.
) else (
    echo    [ERRO] Ambiente virtual 'venv312' nao encontrado!
    pause
    exit /b 1
)
echo.

:: 3. Aguardar inicialização
echo [3/4] Aguardando inicializacao (30 segundos)...
echo.
echo    Backend rodando em: http://localhost:8000
echo    Interface em: http://localhost:8000/static/
echo.

timeout /t 30 /nobreak

:: 4. Abrir Navegador
echo [4/4] Abrindo Interface no Navegador...
start "" "http://localhost:8000/static/"
echo    -> Interface aberta.
echo.

:: Verificar se backend está rodando
tasklist /FI "WINDOWTITLE eq FlashNews Server*" 2>nul | find /I "cmd.exe" >nul

if %ERRORLEVEL% EQU 0 (
    echo ==========================================
    echo      SISTEMA INICIADO COM SUCESSO!
    echo ==========================================
    echo.
    echo ✓ Ollama rodando (IA local)
    echo ✓ Backend rodando (http://localhost:8000)
    echo ✓ Interface aberta no navegador
    echo.
    echo Esta janela fechará em 5 segundos...
    echo Mantenha a janela do servidor (minimizada) aberta.
    timeout /t 5 /nobreak >nul
    exit /b 0
) else (
    echo ==========================================
    echo          ERRO NA INICIALIZACAO
    echo ==========================================
    echo.
    echo ⚠ Backend não está rodando
    echo Verifique os logs na janela minimizada
    pause
    exit /b 1
)
