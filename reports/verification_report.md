# Organizador Avancado de Arquivos 1.5.0 - Verification Report

Generated on 2026-09-01T09:43:19.407413

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

============================= 94 passed in 1.75s ==============================


```

## Coverage Report

```
Name                                                               Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------------------
C:\python\moverarquivos\advanced-organizer\src\document_terms.py      77      3    96%   62, 70, 90
C:\python\moverarquivos\advanced-organizer\src\gui.py                204     31    85%   118-121, 126-127, 129-130, 143, 153, 160, 168, 175-176, 201-202, 213-214, 255-258, 282-286, 290-294
C:\python\moverarquivos\advanced-organizer\src\organizer.py          174     31    82%   111, 115-117, 139-140, 180, 191-193, 258-283
C:\python\moverarquivos\advanced-organizer\src\strategies.py         138      7    95%   23, 37, 39, 61, 74-75, 182
C:\python\moverarquivos\advanced-organizer\src\version.py              2      0   100%
pdf_fixtures.py                                                       35      0   100%
test_document_title.py                                               301      1    99%   494
test_gui.py                                                          163      3    98%   40-41, 243
test_organizer.py                                                    115      1    99%   168
test_regressions.py                                                   55      1    98%   105
test_strategies.py                                                    40      1    98%   60
------------------------------------------------------------------------------------------------
TOTAL                                                               1304     79    94%


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


2026-09-01 09:43:23,873 - INFO - Iniciando organização no diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25 (Modo Simulação: True)
2026-09-01 09:43:23,874 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\Impostos
2026-09-01 09:43:23,874 - WARNING - Caminho não encontrado: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\Notas
2026-09-01 09:43:23,874 - INFO - Processando diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25
2026-09-01 09:43:23,875 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\foto.jpg -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\JPG\foto.jpg
2026-09-01 09:43:23,875 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\planilha.xlsx -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\XLSX\planilha.xlsx
2026-09-01 09:43:23,875 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\relatorio.txt -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\Relatórios\relatorio.txt
2026-09-01 09:43:23,875 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\sem_extensao -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify__s2_ko25\Outros\sem_extensao
2026-09-01 09:43:23,875 - WARNING - SIMULACAO CONCLUIDA: 4 arquivo(s) analisado(s), 4 seriam movidos. NENHUM arquivo foi movido de verdade.
2026-09-01 09:43:23,875 - WARNING - Para mover os arquivos, rode novamente com --real (ou use a interface grafica, que mostra a tabela antes de mover).

```

## Build Script Output

```
exit code: 0
version packaged: 1.5.0
OrganizadorArquivosGUI.exe present: True
executables in dist/: ['OrganizadorArquivosGUI.exe']

Usando interpretador: ..\.venv\Scripts\python.exe

Gerando as propriedades do executavel...
version_info.txt gerado para a versao 1.5.0

Gerando o executavel da INTERFACE GRAFICA...

Build concluido! O executavel esta na pasta 'dist':
  OrganizadorArquivosGUI.exe  - clique duplo para abrir a janela

A linha de comando continua existindo, pelo interpretador:
  "..\.venv\Scripts\python.exe" src\organizer.py --path "C:\alguma\pasta" --report
Pressione qualquer tecla para continuar. . . 

296 INFO: PyInstaller: 6.19.0, contrib hooks: 2026.6
296 INFO: Python: 3.13.14
349 INFO: Platform: Windows-11-10.0.26200-SP0
350 INFO: Python environment: C:\python\moverarquivos\.venv
351 INFO: wrote C:\python\moverarquivos\advanced-organizer\OrganizadorArquivosGUI.spec
360 INFO: Module search paths (PYTHONPATH):
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
1218 INFO: checking Analysis
1253 INFO: Building because C:\python\moverarquivos\advanced-organizer\src\gui.py changed
1253 INFO: Looking for Python shared library...
1253 INFO: Using Python shared library: C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python313.dll
1253 INFO: Running Analysis Analysis-00.toc
1253 INFO: Target bytecode optimization level: 0
1253 INFO: Initializing module dependency graph...
1255 INFO: Initializing module graph hook caches...
1276 INFO: Analyzing modules for base_library.zip ...
3564 INFO: Processing standard module hook 'hook-encodings.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
4788 INFO: Processing standard module hook 'hook-heapq.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
6168 INFO: Processing standard module hook 'hook-pickle.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8223 INFO: Caching module dependency graph...
8260 INFO: Analyzing C:\python\moverarquivos\advanced-organizer\src\gui.py
8289 INFO: Processing pre-find-module-path hook 'hook-tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_find_module_path'
8296 INFO: TclTkInfo: initializing cached Tcl/Tk info...
8948 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9183 INFO: Processing standard module hook 'hook-multiprocessing.util.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9401 INFO: Processing standard module hook 'hook-xml.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9763 INFO: Processing standard module hook 'hook-sysconfig.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9775 INFO: Processing standard module hook 'hook-_ctypes.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9885 INFO: Processing pre-safe-import-module hook 'hook-typing_extensions.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
9891 INFO: SetuptoolsInfo: initializing cached setuptools info...
11822 INFO: Processing standard module hook 'hook-pdfminer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
12689 INFO: Processing standard module hook 'hook-difflib.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
12830 INFO: Processing standard module hook 'hook-cryptography.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
15084 INFO: hook-cryptography: cryptography does not seem to be using dynamically linked OpenSSL.
15417 INFO: Processing standard module hook 'hook-charset_normalizer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
15680 INFO: Processing module hooks (post-graph stage)...
16068 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
16081 INFO: Performing binary vs. data reclassification (1086 entries)
21490 INFO: Looking for ctypes DLLs
21500 INFO: Analyzing run-time hooks ...
21501 INFO: Including run-time hook 'pyi_rth_inspect.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
21509 INFO: Including run-time hook 'pyi_rth_pkgutil.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
21517 INFO: Including run-time hook 'pyi_rth_multiprocessing.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
21522 INFO: Including run-time hook 'pyi_rth_cryptography_openssl.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\rthooks'
21525 INFO: Including run-time hook 'pyi_rth__tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
21563 INFO: Creating base_library.zip...
22059 INFO: Looking for dynamic libraries
22825 INFO: Extra DLL search directories (AddDllDirectory): []
22825 INFO: Extra DLL search directories (PATH): []
23644 INFO: Warnings written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\warn-OrganizadorArquivosGUI.txt
23680 INFO: Graph cross-reference written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\xref-OrganizadorArquivosGUI.html
23811 INFO: checking PYZ
23821 INFO: Building because toc changed
23821 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz
24204 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz completed successfully.
24265 INFO: checking PKG
24306 INFO: Building because toc changed
24306 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg
28929 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg completed successfully.
28969 INFO: Bootloader C:\python\moverarquivos\.venv\Lib\site-packages\PyInstaller\bootloader\Windows-64bit-intel\runw.exe
28969 INFO: checking EXE
28998 INFO: Building because versrsrc changed
28998 INFO: Building EXE from EXE-00.toc
28999 INFO: Copying bootloader EXE to C:\python\moverarquivos\advanced-organizer\dist\OrganizadorArquivosGUI.exe
29078 INFO: Copying icon to EXE
29114 INFO: Copying version information to EXE
29136 INFO: Copying 0 resources to EXE
29136 INFO: Embedding manifest in EXE
29158 INFO: Appending PKG archive to EXE
29180 INFO: Fixing EXE headers
29326 INFO: Building EXE from EXE-00.toc completed successfully.
29366 INFO: Build complete! The results are available in: C:\python\moverarquivos\advanced-organizer\dist

```

