# Organizador Avancado de Arquivos 1.6.0 - Verification Report

Generated on 2026-09-03T17:49:05.339763

## Test Execution (pytest)

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\python\moverarquivos\advanced-organizer\tests
collected 94 items

test_document_title.py ................................................. [ 52%]
...............                                                          [ 68%]
test_gui.py ..................                                           [ 87%]
test_organizer.py ......                                                 [ 93%]
test_regressions.py ...                                                  [ 96%]
test_strategies.py ...                                                   [100%]

============================= 94 passed in 1.65s ==============================


```

## Coverage Report

```
Name                                                               Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------------------
C:\python\moverarquivos\advanced-organizer\src\document_terms.py      77      3    96%   62, 70, 90
C:\python\moverarquivos\advanced-organizer\src\gui.py                205     31    85%   118-121, 126-127, 129-130, 143, 153, 160, 169, 176-177, 202-203, 214-215, 256-259, 283-287, 291-295
C:\python\moverarquivos\advanced-organizer\src\organizer.py          176     31    82%   119, 123-125, 147-148, 188, 199-201, 267-292
C:\python\moverarquivos\advanced-organizer\src\strategies.py         138      7    95%   23, 37, 39, 61, 74-75, 182
C:\python\moverarquivos\advanced-organizer\src\version.py              2      0   100%
pdf_fixtures.py                                                       35      0   100%
test_document_title.py                                               303      1    99%   496
test_gui.py                                                          165      3    98%   40-41, 245
test_organizer.py                                                    115      1    99%   168
test_regressions.py                                                   56      1    98%   107
test_strategies.py                                                    40      1    98%   60
------------------------------------------------------------------------------------------------
TOTAL                                                               1312     79    94%


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


2026-09-03 17:49:09,348 - INFO - Iniciando organização no diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px (Modo Simulação: True)
2026-09-03 17:49:09,349 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\Impostos
2026-09-03 17:49:09,349 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\Notas
2026-09-03 17:49:09,349 - INFO - Processando diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px
2026-09-03 17:49:09,350 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\foto.jpg -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\Arquivos Organizados\JPG\foto.jpg
2026-09-03 17:49:09,350 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\planilha.xlsx -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\Arquivos Organizados\XLSX\planilha.xlsx
2026-09-03 17:49:09,350 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\relatorio.txt -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\Arquivos Organizados\Relatórios\relatorio.txt
2026-09-03 17:49:09,350 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\sem_extensao -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_0dmf14px\Arquivos Organizados\Outros\sem_extensao
2026-09-03 17:49:09,350 - WARNING - SIMULACAO CONCLUIDA: 4 arquivo(s) analisado(s), 4 seriam movidos. NENHUM arquivo foi movido de verdade.
2026-09-03 17:49:09,350 - WARNING - Para mover os arquivos, rode novamente com --real (ou use a interface grafica, que mostra a tabela antes de mover).

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

297 INFO: PyInstaller: 6.19.0, contrib hooks: 2026.6
297 INFO: Python: 3.13.14
346 INFO: Platform: Windows-11-10.0.26200-SP0
347 INFO: Python environment: C:\python\moverarquivos\.venv
347 INFO: wrote C:\python\moverarquivos\advanced-organizer\OrganizadorArquivosGUI.spec
357 INFO: Module search paths (PYTHONPATH):
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
919 INFO: checking Analysis
940 INFO: Building because C:\python\moverarquivos\advanced-organizer\src\gui.py changed
940 INFO: Looking for Python shared library...
940 INFO: Using Python shared library: C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python313.dll
940 INFO: Running Analysis Analysis-00.toc
940 INFO: Target bytecode optimization level: 0
941 INFO: Initializing module dependency graph...
942 INFO: Initializing module graph hook caches...
1038 INFO: Analyzing modules for base_library.zip ...
2675 INFO: Processing standard module hook 'hook-encodings.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
5259 INFO: Processing standard module hook 'hook-pickle.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
6276 INFO: Processing standard module hook 'hook-heapq.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
6910 INFO: Caching module dependency graph...
6951 INFO: Analyzing C:\python\moverarquivos\advanced-organizer\src\gui.py
6979 INFO: Processing pre-find-module-path hook 'hook-tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_find_module_path'
6982 INFO: TclTkInfo: initializing cached Tcl/Tk info...
7647 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
7872 INFO: Processing standard module hook 'hook-multiprocessing.util.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8064 INFO: Processing standard module hook 'hook-xml.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8379 INFO: Processing standard module hook 'hook-sysconfig.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8386 INFO: Processing standard module hook 'hook-_ctypes.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8462 INFO: Processing pre-safe-import-module hook 'hook-typing_extensions.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
8466 INFO: SetuptoolsInfo: initializing cached setuptools info...
10144 INFO: Processing standard module hook 'hook-pdfminer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
10955 INFO: Processing standard module hook 'hook-difflib.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
11080 INFO: Processing standard module hook 'hook-cryptography.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
13051 INFO: hook-cryptography: cryptography does not seem to be using dynamically linked OpenSSL.
13279 INFO: Processing standard module hook 'hook-charset_normalizer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
13489 INFO: Processing module hooks (post-graph stage)...
13783 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
13794 INFO: Performing binary vs. data reclassification (1086 entries)
14407 INFO: Looking for ctypes DLLs
14418 INFO: Analyzing run-time hooks ...
14419 INFO: Including run-time hook 'pyi_rth_inspect.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
14423 INFO: Including run-time hook 'pyi_rth_pkgutil.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
14427 INFO: Including run-time hook 'pyi_rth_multiprocessing.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
14429 INFO: Including run-time hook 'pyi_rth_cryptography_openssl.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\rthooks'
14431 INFO: Including run-time hook 'pyi_rth__tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
14461 INFO: Creating base_library.zip...
14945 INFO: Looking for dynamic libraries
15455 INFO: Extra DLL search directories (AddDllDirectory): []
15455 INFO: Extra DLL search directories (PATH): []
16095 INFO: Warnings written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\warn-OrganizadorArquivosGUI.txt
16126 INFO: Graph cross-reference written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\xref-OrganizadorArquivosGUI.html
16212 INFO: checking PYZ
16227 INFO: Building because C:\python\moverarquivos\advanced-organizer\src\organizer.py changed
16227 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz
16530 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz completed successfully.
16573 INFO: checking PKG
16597 INFO: Building because toc changed
16597 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg
20809 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg completed successfully.
20834 INFO: Bootloader C:\python\moverarquivos\.venv\Lib\site-packages\PyInstaller\bootloader\Windows-64bit-intel\runw.exe
20834 INFO: checking EXE
20851 INFO: Building because versrsrc changed
20851 INFO: Building EXE from EXE-00.toc
20852 INFO: Copying bootloader EXE to C:\python\moverarquivos\advanced-organizer\dist\OrganizadorArquivosGUI.exe
21210 INFO: Copying icon to EXE
21441 INFO: Copying version information to EXE
21715 INFO: Copying 0 resources to EXE
21715 INFO: Embedding manifest in EXE
21972 INFO: Appending PKG archive to EXE
21999 INFO: Fixing EXE headers
22140 INFO: Building EXE from EXE-00.toc completed successfully.
22168 INFO: Build complete! The results are available in: C:\python\moverarquivos\advanced-organizer\dist

```

