@echo off
REM Prefere o interpretador da venv do projeto: e ele que tem as dependencias
REM fixadas em requirements-dev.txt. Sem isso o build usa o Python do PATH e o
REM executavel sai maior, com pacotes que o projeto nao declara.
set PY=python
if exist "..\.venv\Scripts\python.exe" set PY=..\.venv\Scripts\python.exe
echo Usando interpretador: %PY%
echo.

REM Propriedades do arquivo (nome, versao, copyright), derivadas de
REM src\version.py. Sem isto o .exe sai com os campos em branco em
REM Propriedades > Detalhes.
echo Gerando as propriedades do executavel...
"%PY%" gerar_version_info.py
echo.

REM --collect-*: o OCR depende do binario do pdfium (pypdfium2_raw) e das
REM projecoes winrt, carregadas por import dentro de funcao - sem coleta
REM explicita o PyInstaller nao as empacota e o OCR fica desligado no .exe.
echo Gerando o executavel da INTERFACE GRAFICA...
"%PY%" -m PyInstaller --noconfirm --onefile --windowed --name "OrganizadorArquivosGUI" --version-file build\version_info.txt --collect-all pypdfium2 --collect-all pypdfium2_raw --collect-submodules winrt src\gui.py
echo.
echo Build concluido! O executavel esta na pasta 'dist':
echo   OrganizadorArquivosGUI.exe  - clique duplo para abrir a janela
echo.
echo A linha de comando continua existindo, pelo interpretador:
echo   "%PY%" src\organizer.py --path "C:\alguma\pasta" --report
pause
