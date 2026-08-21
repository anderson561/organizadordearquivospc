# MoverArquivos Verification Report

Generated on 2026-08-21T09:38:19.990925

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

============================= 88 passed in 2.45s ==============================


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


2026-08-21 09:38:27,341 - INFO - Iniciando organização no diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8 (Modo Simulação: True)
2026-08-21 09:38:27,341 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\Impostos
2026-08-21 09:38:27,341 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\Notas
2026-08-21 09:38:27,342 - INFO - Processando diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8
2026-08-21 09:38:27,343 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\foto.jpg -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\JPG\foto.jpg
2026-08-21 09:38:27,343 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\planilha.xlsx -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\XLSX\planilha.xlsx
2026-08-21 09:38:27,343 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\relatorio.txt -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\Relatórios\relatorio.txt
2026-08-21 09:38:27,343 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\sem_extensao -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_lyehpzl8\Outros\sem_extensao
2026-08-21 09:38:27,343 - WARNING - SIMULACAO CONCLUIDA: 4 arquivo(s) analisado(s), 4 seriam movidos. NENHUM arquivo foi movido de verdade.
2026-08-21 09:38:27,343 - WARNING - Para mover os arquivos, rode novamente com --real (ou use a interface grafica, que mostra a tabela antes de mover).

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

336 INFO: PyInstaller: 6.19.0, contrib hooks: 2026.6
337 INFO: Python: 3.13.14
398 INFO: Platform: Windows-11-10.0.26200-SP0
398 INFO: Python environment: C:\python\moverarquivos\.venv
400 INFO: wrote C:\python\moverarquivos\advanced-organizer\OrganizadorArquivosGUI.spec
409 INFO: Module search paths (PYTHONPATH):
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
1160 INFO: checking Analysis
1195 INFO: Building because C:\python\moverarquivos\advanced-organizer\src\organizer.py changed
1195 INFO: Looking for Python shared library...
1195 INFO: Using Python shared library: C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python313.dll
1195 INFO: Running Analysis Analysis-00.toc
1195 INFO: Target bytecode optimization level: 0
1196 INFO: Initializing module dependency graph...
1198 INFO: Initializing module graph hook caches...
1302 INFO: Analyzing modules for base_library.zip ...
3720 INFO: Processing standard module hook 'hook-encodings.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
4796 INFO: Processing standard module hook 'hook-heapq.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
6026 INFO: Processing standard module hook 'hook-pickle.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
7611 INFO: Caching module dependency graph...
7652 INFO: Analyzing C:\python\moverarquivos\advanced-organizer\src\gui.py
7681 INFO: Processing pre-find-module-path hook 'hook-tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_find_module_path'
7684 INFO: TclTkInfo: initializing cached Tcl/Tk info...
8243 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8480 INFO: Processing standard module hook 'hook-multiprocessing.util.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8817 INFO: Processing standard module hook 'hook-xml.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9129 INFO: Processing standard module hook 'hook-sysconfig.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9136 INFO: Processing standard module hook 'hook-_ctypes.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9213 INFO: Processing pre-safe-import-module hook 'hook-typing_extensions.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
9217 INFO: SetuptoolsInfo: initializing cached setuptools info...
10919 INFO: Processing standard module hook 'hook-pdfminer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
11691 INFO: Processing standard module hook 'hook-difflib.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
11820 INFO: Processing standard module hook 'hook-cryptography.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
14286 INFO: hook-cryptography: cryptography does not seem to be using dynamically linked OpenSSL.
14517 INFO: Processing standard module hook 'hook-charset_normalizer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
14736 INFO: Processing module hooks (post-graph stage)...
15051 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
15063 INFO: Performing binary vs. data reclassification (1086 entries)
15730 INFO: Looking for ctypes DLLs
15740 INFO: Analyzing run-time hooks ...
15741 INFO: Including run-time hook 'pyi_rth_inspect.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
15745 INFO: Including run-time hook 'pyi_rth_pkgutil.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
15748 INFO: Including run-time hook 'pyi_rth_multiprocessing.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
15751 INFO: Including run-time hook 'pyi_rth_cryptography_openssl.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\rthooks'
15753 INFO: Including run-time hook 'pyi_rth__tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
15787 INFO: Creating base_library.zip...
16271 INFO: Looking for dynamic libraries
16851 INFO: Extra DLL search directories (AddDllDirectory): []
16851 INFO: Extra DLL search directories (PATH): []
17692 INFO: Warnings written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\warn-OrganizadorArquivosGUI.txt
17732 INFO: Graph cross-reference written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\xref-OrganizadorArquivosGUI.html
17852 INFO: checking PYZ
17872 INFO: Building because C:\python\moverarquivos\advanced-organizer\src\organizer.py changed
17872 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz
18310 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz completed successfully.
18353 INFO: checking PKG
18365 INFO: Building because toc changed
18366 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg
23749 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg completed successfully.
23790 INFO: Bootloader C:\python\moverarquivos\.venv\Lib\site-packages\PyInstaller\bootloader\Windows-64bit-intel\runw.exe
23791 INFO: checking EXE
23804 INFO: Building because toc changed
23804 INFO: Building EXE from EXE-00.toc
23806 INFO: Copying bootloader EXE to C:\python\moverarquivos\advanced-organizer\dist\OrganizadorArquivosGUI.exe
23852 INFO: Copying icon to EXE
23883 INFO: Copying 0 resources to EXE
23883 INFO: Embedding manifest in EXE
23917 INFO: Appending PKG archive to EXE
23960 INFO: Fixing EXE headers
24131 INFO: Building EXE from EXE-00.toc completed successfully.
24170 INFO: Build complete! The results are available in: C:\python\moverarquivos\advanced-organizer\dist

```

