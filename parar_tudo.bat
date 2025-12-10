@echo off
title Parar TODOS os Serviços FlashNews
color 0C

echo ==========================================
echo    PARANDO TODOS OS SERVICOS FLASHNEWS
echo ==========================================
echo.

echo [1/4] Parando servidor backend (FastAPI)...
taskkill /F /FI "WINDOWTITLE eq FlashNews Server*" /T 2>NUL
if %ERRORLEVEL% EQU 0 (
    echo    -> Backend parado.
)

REM Parar processos Python na porta 8000 (backend)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo    -> Parando processo na porta 8000...
    taskkill /F /PID %%a 2>NUL
)

echo.
echo [2/4] Parando servidor viewer...
taskkill /F /FI "WINDOWTITLE eq FlashNews Viewer*" /T 2>NUL

echo.
echo [3/4] Parando Ollama...
taskkill /F /IM "ollama.exe" /T 2>NUL
if %ERRORLEVEL% EQU 0 (
    echo    -> Ollama parado.
) else (
    echo    -> Ollama nao estava rodando.
)

echo.
echo [4/4] Limpando processos Python pendentes...
REM Parar todos os python.exe que não são do sistema
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /C:"PID:"') do (
    taskkill /F /PID %%a 2>NUL
)

echo.
echo ==========================================
echo   TODOS OS SERVICOS FORAM PARADOS
echo ==========================================
echo.
echo Esta janela fechara automaticamente em 5 segundos...
timeout /t 5 /nobreak >nul
exit /b 0
