# Organizador Avancado de Arquivos 1.8.0 - Verification Report

Generated on 2026-11-16T15:25:56.155880

## Test Execution (pytest)

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\python\moverarquivos\advanced-organizer\tests
collected 122 items

test_document_title.py ................................................. [ 40%]
....................                                                     [ 56%]
test_gui.py ..................                                           [ 71%]
test_migracao_e_subpastas.py ................                            [ 84%]
test_organizer.py ........                                               [ 90%]
test_regressions.py ....                                                 [ 94%]
test_strategies.py .......                                               [100%]

============================= 122 passed in 3.59s =============================


```

## Coverage Report

```
Name                                                               Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------------------
C:\python\moverarquivos\advanced-organizer\src\document_terms.py      77      3    96%   62, 70, 90
C:\python\moverarquivos\advanced-organizer\src\gui.py                219     41    81%   125-128, 133-134, 136-137, 150, 160, 167, 176, 183-184, 210-211, 222-223, 264-267, 291-295, 299-316
C:\python\moverarquivos\advanced-organizer\src\ocr.py                 74     19    74%   34-36, 45-53, 68, 76, 99, 103, 107-108, 111-113
C:\python\moverarquivos\advanced-organizer\src\organizer.py          231     37    84%   62-63, 168, 172-174, 236-237, 280, 294-296, 319-320, 381-409
C:\python\moverarquivos\advanced-organizer\src\strategies.py         168      6    96%   23, 37, 61, 74-75, 197
C:\python\moverarquivos\advanced-organizer\src\version.py              2      0   100%
pdf_fixtures.py                                                       35      0   100%
scan_fixtures.py                                                      25      0   100%
test_document_title.py                                               341      1    99%   555
test_gui.py                                                          165      3    98%   40-41, 245
test_migracao_e_subpastas.py                                         102      1    99%   147
test_organizer.py                                                    126      1    99%   187
test_regressions.py                                                   70      1    99%   134
test_strategies.py                                                    54      1    98%   87
------------------------------------------------------------------------------------------------
TOTAL                                                               1689    114    93%


```

## Ruff Linting

```
All checks passed!


```

## CLI (dry run smoke test)

```
exit code: 0
dry-run entries logged: 4 (expected 4)
sandbox after run: ['foto.jpg', 'planilha.xlsx', 'relatorio.txt', 'sem_extensao']
sandbox untouched: True


2026-11-16 15:26:02,759 - INFO - Iniciando organização no diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju (Modo Simulação: True)
2026-11-16 15:26:02,759 - INFO - Processando diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju
2026-11-16 15:26:02,761 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju\foto.jpg -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju\Arquivos Organizados\JPG\foto.jpg
2026-11-16 15:26:02,761 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju\planilha.xlsx -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju\Arquivos Organizados\XLSX\planilha.xlsx
2026-11-16 15:26:02,761 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju\relatorio.txt -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju\Arquivos Organizados\Relatórios\relatorio.txt
2026-11-16 15:26:02,761 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju\sem_extensao -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_6uodmiju\Arquivos Organizados\Outros\sem_extensao
2026-11-16 15:26:02,761 - WARNING - SIMULACAO CONCLUIDA: 4 arquivo(s) analisado(s), 4 seriam movidos. NENHUM arquivo foi movido de verdade.
2026-11-16 15:26:02,761 - WARNING - Para mover os arquivos, rode novamente com --real (ou use a interface grafica, que mostra a tabela antes de mover).

```

## Build Script Output

```
exit code: 0
version packaged: 1.8.0
OrganizadorArquivosGUI.exe present: True
executables in dist/: ['OrganizadorArquivosGUI.exe']

Usando interpretador: ..\.venv\Scripts\python.exe

Gerando as propriedades do executavel...
version_info.txt gerado para a versao 1.8.0

Gerando o executavel da INTERFACE GRAFICA...

Build concluido! O executavel esta na pasta 'dist':
  OrganizadorArquivosGUI.exe  - clique duplo para abrir a janela

A linha de comando continua existindo, pelo interpretador:
  "..\.venv\Scripts\python.exe" src\organizer.py --path "C:\alguma\pasta" --report
Pressione qualquer tecla para continuar. . . 

290 INFO: PyInstaller: 6.19.0, contrib hooks: 2026.6
290 INFO: Python: 3.13.14
343 INFO: Platform: Windows-11-10.0.26300-SP0
343 INFO: Python environment: C:\python\moverarquivos\.venv
344 INFO: wrote C:\python\moverarquivos\advanced-organizer\OrganizadorArquivosGUI.spec
3454 INFO: Module search paths (PYTHONPATH):
['C:\\python\\moverarquivos\\advanced-organizer',
 'C:\\Program '
 'Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\\python313.zip',
 'C:\\Program '
 'Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\\DLLs',
 'C:\\Program '
 'Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\\Lib',
 'C:\\Program '
 'Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0',
 'C:\\python\\moverarquivos\\.venv',
 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages',
 'C:\\python\\moverarquivos\\advanced-organizer\\src']
4096 INFO: Appending 'binaries' from .spec
4097 INFO: Appending 'datas' from .spec
4111 INFO: checking Analysis
4251 INFO: checking PYZ
4299 INFO: checking PKG
4387 INFO: Bootloader C:\python\moverarquivos\.venv\Lib\site-packages\PyInstaller\bootloader\Windows-64bit-intel\runw.exe
4387 INFO: checking EXE
4401 INFO: Build complete! The results are available in: C:\python\moverarquivos\advanced-organizer\dist

```

