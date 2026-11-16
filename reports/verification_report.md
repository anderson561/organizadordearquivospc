# Organizador Avancado de Arquivos 1.6.0 - Verification Report

Generated on 2026-11-16T13:51:49.018159

## Test Execution (pytest)

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\python\moverarquivos\advanced-organizer\tests
collected 95 items

test_document_title.py ................................................. [ 51%]
...............                                                          [ 67%]
test_gui.py ..................                                           [ 86%]
test_organizer.py ......                                                 [ 92%]
test_regressions.py ....                                                 [ 96%]
test_strategies.py ...                                                   [100%]

============================= 95 passed in 2.22s ==============================


```

## Coverage Report

```
Name                                                               Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------------------
C:\python\moverarquivos\advanced-organizer\src\document_terms.py      77      3    96%   62, 70, 90
C:\python\moverarquivos\advanced-organizer\src\gui.py                205     31    85%   118-121, 126-127, 129-130, 143, 153, 160, 169, 176-177, 202-203, 214-215, 256-259, 283-287, 291-295
C:\python\moverarquivos\advanced-organizer\src\organizer.py          175     31    82%   119, 123-125, 147-148, 188, 202-204, 270-295
C:\python\moverarquivos\advanced-organizer\src\strategies.py         138      7    95%   23, 37, 39, 61, 74-75, 182
C:\python\moverarquivos\advanced-organizer\src\version.py              2      0   100%
pdf_fixtures.py                                                       35      0   100%
test_document_title.py                                               303      1    99%   496
test_gui.py                                                          165      3    98%   40-41, 245
test_organizer.py                                                    115      1    99%   168
test_regressions.py                                                   72      1    99%   136
test_strategies.py                                                    40      1    98%   60
------------------------------------------------------------------------------------------------
TOTAL                                                               1327     79    94%


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


2026-11-16 13:51:55,420 - INFO - Iniciando organização no diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j (Modo Simulação: True)
2026-11-16 13:51:55,421 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\Impostos
2026-11-16 13:51:55,421 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\Notas
2026-11-16 13:51:55,421 - INFO - Processando diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j
2026-11-16 13:51:55,422 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\foto.jpg -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\Arquivos Organizados\JPG\foto.jpg
2026-11-16 13:51:55,422 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\planilha.xlsx -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\Arquivos Organizados\XLSX\planilha.xlsx
2026-11-16 13:51:55,422 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\relatorio.txt -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\Arquivos Organizados\Relatórios\relatorio.txt
2026-11-16 13:51:55,422 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\sem_extensao -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_5d_5r95j\Arquivos Organizados\Outros\sem_extensao
2026-11-16 13:51:55,423 - WARNING - SIMULACAO CONCLUIDA: 4 arquivo(s) analisado(s), 4 seriam movidos. NENHUM arquivo foi movido de verdade.
2026-11-16 13:51:55,423 - WARNING - Para mover os arquivos, rode novamente com --real (ou use a interface grafica, que mostra a tabela antes de mover).

```

## Build Script Output

```
exit code: 0
version packaged: 1.6.0
OrganizadorArquivosGUI.exe present: True
executables in dist/: ['OrganizadorArquivosGUI.exe']

Usando interpretador: ..\.venv\Scripts\python.exe

Gerando as propriedades do executavel...
version_info.txt gerado para a versao 1.6.0

Gerando o executavel da INTERFACE GRAFICA...

Build concluido! O executavel esta na pasta 'dist':
  OrganizadorArquivosGUI.exe  - clique duplo para abrir a janela

A linha de comando continua existindo, pelo interpretador:
  "..\.venv\Scripts\python.exe" src\organizer.py --path "C:\alguma\pasta" --report
Pressione qualquer tecla para continuar. . . 

357 INFO: PyInstaller: 6.19.0, contrib hooks: 2026.6
357 INFO: Python: 3.13.14
409 INFO: Platform: Windows-11-10.0.26300-SP0
409 INFO: Python environment: C:\python\moverarquivos\.venv
410 INFO: wrote C:\python\moverarquivos\advanced-organizer\OrganizadorArquivosGUI.spec
419 INFO: Module search paths (PYTHONPATH):
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
1080 INFO: Building because C:\python\moverarquivos\advanced-organizer\src\organizer.py changed
1080 INFO: Looking for Python shared library...
1080 INFO: Using Python shared library: C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python313.dll
1080 INFO: Running Analysis Analysis-00.toc
1080 INFO: Target bytecode optimization level: 0
1080 INFO: Initializing module dependency graph...
1082 INFO: Initializing module graph hook caches...
1184 INFO: Analyzing modules for base_library.zip ...
3601 INFO: Processing standard module hook 'hook-encodings.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
4621 INFO: Processing standard module hook 'hook-heapq.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
6058 INFO: Processing standard module hook 'hook-pickle.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
7830 INFO: Caching module dependency graph...
7874 INFO: Analyzing C:\python\moverarquivos\advanced-organizer\src\gui.py
7919 INFO: Processing pre-find-module-path hook 'hook-tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_find_module_path'
7925 INFO: TclTkInfo: initializing cached Tcl/Tk info...
8651 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8868 INFO: Processing standard module hook 'hook-multiprocessing.util.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9070 INFO: Processing standard module hook 'hook-xml.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9377 INFO: Processing standard module hook 'hook-sysconfig.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9384 INFO: Processing standard module hook 'hook-_ctypes.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9462 INFO: Processing pre-safe-import-module hook 'hook-typing_extensions.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
9465 INFO: SetuptoolsInfo: initializing cached setuptools info...
11229 INFO: Processing standard module hook 'hook-pdfminer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
12044 INFO: Processing standard module hook 'hook-difflib.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
12175 INFO: Processing standard module hook 'hook-cryptography.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
14372 INFO: hook-cryptography: cryptography does not seem to be using dynamically linked OpenSSL.
14611 INFO: Processing standard module hook 'hook-charset_normalizer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
14820 INFO: Processing module hooks (post-graph stage)...
15145 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
15165 INFO: Performing binary vs. data reclassification (1086 entries)
17553 INFO: Looking for ctypes DLLs
17563 INFO: Analyzing run-time hooks ...
17564 INFO: Including run-time hook 'pyi_rth_inspect.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
17568 INFO: Including run-time hook 'pyi_rth_pkgutil.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
17571 INFO: Including run-time hook 'pyi_rth_multiprocessing.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
17574 INFO: Including run-time hook 'pyi_rth_cryptography_openssl.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\rthooks'
17576 INFO: Including run-time hook 'pyi_rth__tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
17609 INFO: Creating base_library.zip...
18134 INFO: Looking for dynamic libraries
18889 INFO: Extra DLL search directories (AddDllDirectory): []
18889 INFO: Extra DLL search directories (PATH): []
19512 INFO: Warnings written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\warn-OrganizadorArquivosGUI.txt
19545 INFO: Graph cross-reference written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\xref-OrganizadorArquivosGUI.html
19628 INFO: checking PYZ
19644 INFO: Building because C:\python\moverarquivos\advanced-organizer\src\organizer.py changed
19644 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz
19957 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz completed successfully.
19987 INFO: checking PKG
19998 INFO: Building because toc changed
19998 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg
24723 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg completed successfully.
24749 INFO: Bootloader C:\python\moverarquivos\.venv\Lib\site-packages\PyInstaller\bootloader\Windows-64bit-intel\runw.exe
24749 INFO: checking EXE
24762 INFO: Building because toc changed
24762 INFO: Building EXE from EXE-00.toc
24764 INFO: Copying bootloader EXE to C:\python\moverarquivos\advanced-organizer\dist\OrganizadorArquivosGUI.exe
25391 INFO: Copying icon to EXE
25645 INFO: Copying version information to EXE
25920 INFO: Copying 0 resources to EXE
25920 INFO: Embedding manifest in EXE
26176 INFO: Appending PKG archive to EXE
26203 INFO: Fixing EXE headers
26349 INFO: Building EXE from EXE-00.toc completed successfully.
26375 INFO: Build complete! The results are available in: C:\python\moverarquivos\advanced-organizer\dist

```

