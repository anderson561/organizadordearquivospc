@echo off
REM Prefere o interpretador da venv do projeto: e ele que tem as dependencias
REM fixadas em requirements-dev.txt. Sem isso o build usa o Python do PATH e o
REM executavel sai maior, com pacotes que o projeto nao declara.
set PY=python
if exist "..\.venv\Scripts\python.exe" set PY=..\.venv\Scripts\python.exe
echo Usando interpretador: %PY%
echo.

echo Gerando o executavel da INTERFACE GRAFICA...
"%PY%" -m PyInstaller --noconfirm --onefile --windowed --name "OrganizadorArquivosGUI" src\gui.py
echo.
echo Build concluido! O executavel esta na pasta 'dist':
echo   OrganizadorArquivosGUI.exe  - clique duplo para abrir a janela
echo.
echo A linha de comando continua existindo, pelo interpretador:
echo   "%PY%" src\organizer.py --path "C:\alguma\pasta" --report
pause
