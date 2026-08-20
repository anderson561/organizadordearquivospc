# MoverArquivos Verification Report

Generated on 2026-08-20T11:18:10.177788

## Test Execution (pytest)

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\python\moverarquivos\advanced-organizer\tests
collected 13 items

test_organizer.py ......                                                 [ 46%]
test_regressions.py ...                                                  [ 69%]
test_strategies.py ....                                                  [100%]

============================= 13 passed in 0.54s ==============================


```

## Coverage Report

```
Name                                                           Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------
C:\python\moverarquivos\advanced-organizer\src\organizer.py       95     24    75%   94, 98-100, 124, 128-129, 132-152
C:\python\moverarquivos\advanced-organizer\src\strategies.py      66      1    98%   20
test_organizer.py                                                115      1    99%   168
test_regressions.py                                               55      1    98%   105
test_strategies.py                                                54      1    98%   87
--------------------------------------------------------------------------------------------
TOTAL                                                            385     28    93%


```

## Ruff Linting

```
All checks passed!


```

## Executable (dry run smoke test)

```
exit code: 0
dry-run entries logged: 4 (expected 4)
sandbox after run: ['foto.jpg', 'planilha.xlsx', 'relatorio.txt', 'sem_extensao']
sandbox untouched: True


2026-08-20 11:18:20,544 - INFO - Iniciando organização no diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a (Modo Simulação: True)
2026-08-20 11:18:20,544 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\Impostos
2026-08-20 11:18:20,544 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\Notas
2026-08-20 11:18:20,545 - INFO - Processando diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a
2026-08-20 11:18:20,545 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\foto.jpg -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\JPG\foto.jpg
2026-08-20 11:18:20,545 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\planilha.xlsx -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\XLSX\planilha.xlsx
2026-08-20 11:18:20,545 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\relatorio.txt -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\TXT\relatorio.txt
2026-08-20 11:18:20,546 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\sem_extensao -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__9ccj2_a\Outros\sem_extensao

```

## Build Script Output

```
Gerando executavel do Organizador Avancado...
Build concluido! O executavel esta na pasta 'dist'.
Pressione qualquer tecla para continuar. . . 

285 INFO: PyInstaller: 6.19.0, contrib hooks: 2026.3
285 INFO: Python: 3.13.14
380 INFO: Platform: Windows-11-10.0.26200-SP0
380 INFO: Python environment: C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0
385 INFO: wrote C:\python\moverarquivos\advanced-organizer\OrganizadorArquivos.spec
399 INFO: Module search paths (PYTHONPATH):
['C:\\python\\moverarquivos\\advanced-organizer',
 'C:\\Program '
 'Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\\python313.zip',
 'C:\\Program '
 'Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\\DLLs',
 'C:\\Program '
 'Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\\Lib',
 'C:\\Program '
 'Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0',
 'C:\\Users\\ANDERSON\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python313\\site-packages',
 'C:\\Program '
 'Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\\Lib\\site-packages',
 'C:\\python\\moverarquivos\\advanced-organizer\\src']
1369 INFO: Appending 'datas' from .spec
1371 INFO: checking Analysis
1574 INFO: checking PYZ
1642 INFO: checking PKG
1729 INFO: Bootloader C:\Users\ANDERSON\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\PyInstaller\bootloader\Windows-64bit-intel\run.exe
1729 INFO: checking EXE
1741 INFO: Build complete! The results are available in: C:\python\moverarquivos\advanced-organizer\dist

```

