# Organizador Avancado de Arquivos 1.7.0 - Verification Report

Generated on 2026-11-16T14:08:23.883360

## Test Execution (pytest)

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\python\moverarquivos\advanced-organizer\tests
collected 101 items

test_document_title.py ................................................. [ 48%]
...............                                                          [ 63%]
test_gui.py ..................                                           [ 81%]
test_organizer.py ........                                               [ 89%]
test_regressions.py ....                                                 [ 93%]
test_strategies.py .......                                               [100%]

============================= 101 passed in 2.27s =============================


```

## Coverage Report

```
Name                                                               Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------------------
C:\python\moverarquivos\advanced-organizer\src\document_terms.py      77      3    96%   62, 70, 90
C:\python\moverarquivos\advanced-organizer\src\gui.py                205     31    85%   118-121, 126-127, 129-130, 143, 153, 160, 169, 176-177, 202-203, 214-215, 256-259, 283-287, 291-295
C:\python\moverarquivos\advanced-organizer\src\organizer.py          177     32    82%   123, 127-129, 151-152, 192, 206-208, 276-302
C:\python\moverarquivos\advanced-organizer\src\strategies.py         159      7    96%   22, 36, 38, 60, 73-74, 181
C:\python\moverarquivos\advanced-organizer\src\version.py              2      0   100%
pdf_fixtures.py                                                       35      0   100%
test_document_title.py                                               303      1    99%   496
test_gui.py                                                          165      3    98%   40-41, 245
test_organizer.py                                                    126      1    99%   187
test_regressions.py                                                   70      1    99%   134
test_strategies.py                                                    54      1    98%   87
------------------------------------------------------------------------------------------------
TOTAL                                                               1373     80    94%


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


2026-11-16 14:08:29,191 - INFO - Iniciando organização no diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl (Modo Simulação: True)
2026-11-16 14:08:29,192 - INFO - Processando diretório: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl
2026-11-16 14:08:29,194 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl\foto.jpg -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl\Arquivos Organizados\JPG\foto.jpg
2026-11-16 14:08:29,194 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl\planilha.xlsx -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl\Arquivos Organizados\XLSX\planilha.xlsx
2026-11-16 14:08:29,194 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl\relatorio.txt -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl\Arquivos Organizados\Relatórios\relatorio.txt
2026-11-16 14:08:29,194 - INFO - [DRY RUN] Moveria: C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl\sem_extensao -> C:\Users\ANDERSON\AppData\Local\Temp\moverarquivos_verify_9e0hm9dl\Arquivos Organizados\Outros\sem_extensao
2026-11-16 14:08:29,194 - WARNING - SIMULACAO CONCLUIDA: 4 arquivo(s) analisado(s), 4 seriam movidos. NENHUM arquivo foi movido de verdade.
2026-11-16 14:08:29,194 - WARNING - Para mover os arquivos, rode novamente com --real (ou use a interface grafica, que mostra a tabela antes de mover).

```

## Build Script Output

```
exit code: 0
version packaged: 1.7.0
OrganizadorArquivosGUI.exe present: True
executables in dist/: ['OrganizadorArquivosGUI.exe']

Usando interpretador: ..\.venv\Scripts\python.exe

Gerando as propriedades do executavel...
version_info.txt gerado para a versao 1.7.0

Gerando o executavel da INTERFACE GRAFICA...

Build concluido! O executavel esta na pasta 'dist':
  OrganizadorArquivosGUI.exe  - clique duplo para abrir a janela

A linha de comando continua existindo, pelo interpretador:
  "..\.venv\Scripts\python.exe" src\organizer.py --path "C:\alguma\pasta" --report
Pressione qualquer tecla para continuar. . . 

341 INFO: PyInstaller: 6.19.0, contrib hooks: 2026.6
341 INFO: Python: 3.13.14
400 INFO: Platform: Windows-11-10.0.26300-SP0
400 INFO: Python environment: C:\python\moverarquivos\.venv
402 INFO: wrote C:\python\moverarquivos\advanced-organizer\OrganizadorArquivosGUI.spec
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
1018 INFO: checking Analysis
1047 INFO: Building because C:\python\moverarquivos\advanced-organizer\src\version.py changed
1047 INFO: Looking for Python shared library...
1047 INFO: Using Python shared library: C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\python313.dll
1047 INFO: Running Analysis Analysis-00.toc
1047 INFO: Target bytecode optimization level: 0
1047 INFO: Initializing module dependency graph...
1049 INFO: Initializing module graph hook caches...
1154 INFO: Analyzing modules for base_library.zip ...
3099 INFO: Processing standard module hook 'hook-encodings.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
5732 INFO: Processing standard module hook 'hook-pickle.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
6771 INFO: Processing standard module hook 'hook-heapq.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
7570 INFO: Caching module dependency graph...
7619 INFO: Analyzing C:\python\moverarquivos\advanced-organizer\src\gui.py
7648 INFO: Processing pre-find-module-path hook 'hook-tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_find_module_path'
7650 INFO: TclTkInfo: initializing cached Tcl/Tk info...
8272 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8517 INFO: Processing standard module hook 'hook-multiprocessing.util.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8783 INFO: Processing standard module hook 'hook-xml.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9131 INFO: Processing standard module hook 'hook-sysconfig.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9143 INFO: Processing standard module hook 'hook-_ctypes.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
9242 INFO: Processing pre-safe-import-module hook 'hook-typing_extensions.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
9244 INFO: SetuptoolsInfo: initializing cached setuptools info...
11148 INFO: Processing standard module hook 'hook-pdfminer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
11953 INFO: Processing standard module hook 'hook-difflib.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
12094 INFO: Processing standard module hook 'hook-cryptography.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
14651 INFO: hook-cryptography: cryptography does not seem to be using dynamically linked OpenSSL.
14996 INFO: Processing standard module hook 'hook-charset_normalizer.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
15227 INFO: Processing module hooks (post-graph stage)...
15525 INFO: Processing standard module hook 'hook-_tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
15537 INFO: Performing binary vs. data reclassification (1086 entries)
16179 INFO: Looking for ctypes DLLs
16190 INFO: Analyzing run-time hooks ...
16191 INFO: Including run-time hook 'pyi_rth_inspect.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
16195 INFO: Including run-time hook 'pyi_rth_pkgutil.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
16199 INFO: Including run-time hook 'pyi_rth_multiprocessing.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
16202 INFO: Including run-time hook 'pyi_rth_cryptography_openssl.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\rthooks'
16205 INFO: Including run-time hook 'pyi_rth__tkinter.py' from 'C:\\python\\moverarquivos\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
16244 INFO: Creating base_library.zip...
16752 INFO: Looking for dynamic libraries
17372 INFO: Extra DLL search directories (AddDllDirectory): []
17372 INFO: Extra DLL search directories (PATH): []
18003 INFO: Warnings written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\warn-OrganizadorArquivosGUI.txt
18035 INFO: Graph cross-reference written to C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\xref-OrganizadorArquivosGUI.html
18112 INFO: checking PYZ
18127 INFO: Building because C:\python\moverarquivos\advanced-organizer\src\organizer.py changed
18127 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz
18470 INFO: Building PYZ (ZlibArchive) C:\python\moverarquivos\advanced-organizer\build\OrganizadorArquivosGUI\PYZ-00.pyz completed successfully.
18507 INFO: checking PKG
18521 INFO: Building because toc changed
18521 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg
23169 INFO: Building PKG (CArchive) OrganizadorArquivosGUI.pkg completed successfully.
23197 INFO: Bootloader C:\python\moverarquivos\.venv\Lib\site-packages\PyInstaller\bootloader\Windows-64bit-intel\runw.exe
23197 INFO: checking EXE
23212 INFO: Building because versrsrc changed
23213 INFO: Building EXE from EXE-00.toc
23214 INFO: Copying bootloader EXE to C:\python\moverarquivos\advanced-organizer\dist\OrganizadorArquivosGUI.exe
23485 INFO: Copying icon to EXE
23713 INFO: Copying version information to EXE
23983 INFO: Copying 0 resources to EXE
23983 INFO: Embedding manifest in EXE
24239 INFO: Appending PKG archive to EXE
24267 INFO: Fixing EXE headers
24407 INFO: Building EXE from EXE-00.toc completed successfully.
24433 INFO: Build complete! The results are available in: C:\python\moverarquivos\advanced-organizer\dist

```

