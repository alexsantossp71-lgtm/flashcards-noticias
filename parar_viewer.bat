@echo off
title Parar FlashNews Viewer
color 0C

echo ==========================================
echo       PARANDO FLASHNEWS VIEWER
echo ==========================================
echo.

echo [1/1] Parando servidor HTTP do visualizador...
taskkill /F /FI "WINDOWTITLE eq FlashNews Viewer*" /T 2>NUL
if %ERRORLEVEL% EQU 0 (
    echo    -> Viewer parado (janela).
)

REM Parar qualquer servidor Python na porta 8001 (viewer)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001 ^| findstr LISTENING') do (
    echo    -> Parando processo na porta 8001...
    taskkill /F /PID %%a 2>NUL
    if %ERRORLEVEL% EQU 0 (
        echo    -> Processo parado com sucesso.
    )
)

echo.
echo ==========================================
echo      VIEWER PARADO COM SUCESSO
echo ==========================================
echo.
echo Esta janela fechara automaticamente em 5 segundos...
timeout /t 5 /nobreak >nul
exit /b 0
