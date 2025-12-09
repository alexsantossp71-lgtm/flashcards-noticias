@echo off
title Parar FlashNews AI
color 0C

echo ==========================================
echo       PARANDO FLASHNEWS AI
echo ==========================================
echo.

echo [1/2] Parando servidor Flask/FastAPI...
taskkill /F /FI "WINDOWTITLE eq FlashNews Server*" /T 2>NUL
if %ERRORLEVEL% EQU 0 (
    echo    -> Servidor parado.
) else (
    echo    -> Servidor nao estava rodando.
)
echo.

echo [2/2] Parando Ollama...
taskkill /F /IM "ollama.exe" /T 2>NUL
if %ERRORLEVEL% EQU 0 (
    echo    -> Ollama parado.
) else (
    echo    -> Ollama nao estava rodando.
)
echo.

echo ==========================================
echo      SERVICOS PARADOS COM SUCESSO
echo ==========================================
echo.
echo Esta janela fechara automaticamente em 10 segundos...
timeout /t 10 /nobreak >nul
exit /b 0
