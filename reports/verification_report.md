# MoverArquivos Verification Report

Generated on 2026-08-21T09:05:04.404389

## Test Execution (pytest)

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\python\moverarquivos\advanced-organizer\tests
collected 88 items

test_document_title.py ................................................. [ 55%]
.........                                                                [ 65%]
test_gui.py ..................                                           [ 86%]
test_organizer.py ......                                                 [ 93%]
test_regressions.py ...                                                  [ 96%]
test_strategies.py ...                                                   [100%]

============================= 88 passed in 2.29s ==============================


```

## Coverage Report

```
Name                                                               Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------------------
C:\python\moverarquivos\advanced-organizer\src\document_terms.py      77      3    96%   62, 70, 90
C:\python\moverarquivos\advanced-organizer\src\gui.py                203     31    85%   117-120, 125-126, 128-129, 142, 152, 159, 167, 174-175, 200-201, 212-213, 254-257, 281-285, 289-293
C:\python\moverarquivos\advanced-organizer\src\organizer.py          172     30    83%   110, 114-116, 138-139, 179, 190-192, 257-281
C:\python\moverarquivos\advanced-organizer\src\strategies.py         138      7    95%   23, 37, 39, 61, 74-75, 182
pdf_fixtures.py                                                       35      0   100%
test_document_title.py                                               276      1    99%   440
test_gui.py                                                          163      3    98%   40-41, 243
test_organizer.py                                                    115      1    99%   168
test_regressions.py                                                   55      1    98%   105
test_strategies.py                                                    40      1    98%   60
------------------------------------------------------------------------------------------------
TOTAL                                                               1274     78    94%


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


2026-08-21 09:05:10,311 - INFO - Iniciando organização no diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w (Modo Simulação: True)
2026-08-21 09:05:10,311 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\Impostos
2026-08-21 09:05:10,312 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\Notas
2026-08-21 09:05:10,312 - INFO - Processando diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w
2026-08-21 09:05:10,313 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\foto.jpg -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\JPG\foto.jpg
2026-08-21 09:05:10,313 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\planilha.xlsx -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\XLSX\planilha.xlsx
2026-08-21 09:05:10,313 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\relatorio.txt -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\Relatórios\relatorio.txt
2026-08-21 09:05:10,313 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\sem_extensao -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_jk0aus8w\Outros\sem_extensao
2026-08-21 09:05:10,313 - WARNING - SIMULACAO CONCLUIDA: 4 arquivo(s) analisado(s), 4 seriam movidos. NENHUM arquivo foi movido de verdade.
2026-08-21 09:05:10,313 - WARNING - Para mover os arquivos, rode novamente com --real (ou use o atalho executar_real.bat).

```

## Build Script Output

```
exit code: 0
OrganizadorArquivosGUI.exe present: True
executables in dist/: ['OrganizadorArquivosGUI.exe']

Usando interpretador: ..\.venv\Scripts\python.exe

Gerando o executavel da INTERFACE GRAFICA...

Build concluido! O executavel esta na pasta 'dist':
  OrganizadorArquivosGUI.exe  - clique duplo para abrir a janela

A linha de comando continua existindo, pelo interpretador:
  "..\.venv\Scripts\python.exe" src\organizer.py --path "C:\alguma\pasta" --report
Pressione qualquer tecla para continuar. . . 

344 INFO: PyInstaller: 6.19.0, contrib hooks: 2026.6
344 INFO: Python: 3.13.14
397 INFO: Platform: Windows-11-10.0.26200-SP0
397 INFO: Python environment: C:\python\moverarquivos\.venv
401 INFO: wrote C:\python\moverarquivos\advanced-organizer\OrganizadorArquivosGUI.spec
410 INFO: Module search paths (PYTHONPATH):
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
1037 INFO: checking Analysis
1201 INFO: checking PYZ
1243 INFO: checking PKG
1324 INFO: Bootloader C:\python\moverarquivos\.venv\Lib\site-packages\PyInstaller\bootloader\Windows-64bit-intel\runw.exe
1325 INFO: checking EXE
1335 INFO: Build complete! The results are available in: C:\python\moverarquivos\advanced-organizer\dist

```

