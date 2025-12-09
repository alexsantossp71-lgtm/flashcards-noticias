@echo off
title Limpeza de Modelos NAO Usados
color 0E

echo ==========================================
echo   LIMPANDO MODELOS NAO UTILIZADOS
echo ==========================================
echo.

set "HF_DIR=%USERPROFILE%\.cache\huggingface\hub"

echo Diretorio de modelos: %HF_DIR%
echo.

if not exist "%HF_DIR%" (
    echo [AVISO] Pasta de modelos nao existe.
    pause
    exit
)

echo MODELOS A MANTER:
echo - RunDiffusion--Juggernaut-XL-Lightning
echo - black-forest-labs--FLUX.1-dev
echo - CompVis--stable-diffusion-safety-checker
echo.
echo TODOS OS OUTROS MODELOS SERAO APAGADOS!
echo.
echo Estimativa de espaco a liberar: 40-60 GB
echo.

pause

echo.
echo Iniciando limpeza...
echo.

REM Listar e deletar modelos não desejados
for /d %%D in ("%HF_DIR%\models--*") do (
    set "MODEL_NAME=%%~nxD"
    
    REM Verifica se NÃO é um dos modelos a manter
    echo !MODEL_NAME! | findstr /i "Juggernaut-XL-Lightning FLUX.1-dev stable-diffusion-safety-checker" >nul
    if errorlevel 1 (
        echo Apagando: %%~nxD
        rd /s /q "%%D" 2>nul
        if errorlevel 1 (
            echo    [ERRO] Nao foi possivel apagar %%~nxD
        ) else (
            echo    [OK] Apagado com sucesso
        )
    ) else (
        echo Mantendo: %%~nxD
    )
)

echo.
echo ==========================================
echo   LIMPEZA CONCLUIDA!
echo ==========================================
echo.
echo Modelos mantidos:
dir /b "%HF_DIR%\models--*" 2>nul
echo.

pause
