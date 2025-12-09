@echo off
setlocal enabledelayedexpansion
title Mover Modelos LIMPOS para F:
color 0B

echo ==========================================
echo   MOVENDO MODELOS PARA F: (LIMPOS)
echo ==========================================
echo.

set "SOURCE=%USERPROFILE%\.cache\huggingface"
set "DEST=F:\AI_Models\huggingface"

echo Origem: %SOURCE%
echo Destino: %DEST%
echo.

if not exist "%SOURCE%" (
    echo [AVISO] Pasta de origem nao existe.
    pause
    exit
)

echo Criando diretorio destino...
mkdir "%DEST%" 2>NUL

echo.
echo IMPORTANTE: Certifique-se de que rodou limpar_modelos.bat ANTES!
echo.
echo Modelos que serao movidos:
dir /b "%SOURCE%\hub\models--*" 2>nul
echo.

pause

echo.
echo Movendo arquivos (pode demorar alguns minutos)...
echo.

REM Usar robocopy com progresso visível
robocopy "%SOURCE%" "%DEST%" /E /MOVE /R:3 /W:5 /MT:8

if %ERRORLEVEL% LEQ 1 (
    echo.
    echo ==========================================
    echo   MODELOS MOVIDOS COM SUCESSO!
    echo ==========================================
    echo.
    echo Modelos agora estao em: %DEST%
    echo.
    echo Espaco liberado no C: drive
    echo.
    echo PROXIMOS PASSOS:
    echo 1. Feche esta janela
    echo 2. Execute: iniciar_flashnews.bat
    echo 3. Teste a geracao de imagens
) else (
    echo.
    echo [ERRO] Algo deu errado durante a movimentacao.
    echo Codigo de erro: %ERRORLEVEL%
)

echo.
pause
