@echo off
title Apagar TODOS os Modelos de IA
color 0C

echo ==========================================
echo   APAGAR TODOS OS MODELOS DE IA
echo ==========================================
echo.
echo AVISO: Isso vai deletar PERMANENTEMENTE:
echo - Todos os modelos em C:\Users\%USERNAME%\.cache\huggingface
echo - Todos os modelos em F:\AI_Models\huggingface
echo.
echo Espaco total a ser liberado: ~20-80 GB
echo.
echo IMPORTANTE: Voce tera que baixar os modelos novamente
echo quando precisar gerar imagens!
echo.

pause

echo.
echo [1/2] Apagando modelos de C: drive...
if exist "%USERPROFILE%\.cache\huggingface" (
    rd /s /q "%USERPROFILE%\.cache\huggingface"
    if errorlevel 1 (
        echo    [ERRO] Nao foi possivel apagar de C:
    ) else (
        echo    [OK] Modelos de C: apagados
    )
) else (
    echo    [INFO] Nenhum modelo encontrado em C:
)

echo.
echo [2/2] Apagando modelos de F: drive...
if exist "F:\AI_Models\huggingface" (
    rd /s /q "F:\AI_Models\huggingface"
    if errorlevel 1 (
        echo    [ERRO] Nao foi possivel apagar de F:
    ) else (
        echo    [OK] Modelos de F: apagados
    )
) else (
    echo    [INFO] Nenhum modelo encontrado em F:
)

echo.
echo ==========================================
echo   LIMPEZA CONCLUIDA!
echo ==========================================
echo.
echo PROXIMOS PASSOS:
echo 1. Execute iniciar_flashnews.bat
echo 2. Ao gerar a primeira imagem, o modelo sera baixado automaticamente
echo 3. Isso levara ~10-15 minutos na primeira vez
echo.

pause
