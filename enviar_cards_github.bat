@echo off
echo ====================================
echo   Enviar Cards para GitHub
echo ====================================
echo.

REM Verificar se há mudanças
git status generated_posts/

echo.
echo Deseja adicionar e enviar estes cards para o GitHub?
echo.
set /p CONFIRM="Digite 's' para confirmar ou qualquer tecla para cancelar: "

if /i not "%CONFIRM%"=="s" (
    echo.
    echo Operacao cancelada.
    pause
    exit /b 0
)

echo.
echo Gerando index posts.json...
python generate_posts_index.py

if errorlevel 1 (
    echo.
    echo AVISO: Erro ao gerar posts.json, mas continuando...
)

echo.
echo Adicionando arquivos...
git add generated_posts/

echo.
echo Verificando mudancas...
git status --short

echo.
set /p COMMIT_MSG="Digite uma mensagem para o commit (ou Enter para mensagem padrao): "

if "%COMMIT_MSG%"=="" (
    REM Mensagem padrão com timestamp
    for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
    set COMMIT_MSG=Add new flashcards generated on %datetime:~0,8%
)

echo.
echo Fazendo commit: %COMMIT_MSG%
git commit -m "%COMMIT_MSG%"

if errorlevel 1 (
    echo.
    echo ERRO: Commit falhou ou nao ha mudancas para commitar.
    pause
    exit /b 1
)

echo.
echo Enviando para GitHub...
git push

if errorlevel 1 (
    echo.
    echo ERRO: Push falhou. Verifique sua conexao e credenciais.
    pause
    exit /b 1
)

echo.
echo ====================================
echo   ✓ Cards enviados com sucesso!
echo ====================================
echo.
echo Aguarde 1-2 minutos para o GitHub Pages atualizar.
echo Depois acesse: https://alexsantossp71-lgtm.github.io/flashcards-noticias/viewer/
echo.

pause
