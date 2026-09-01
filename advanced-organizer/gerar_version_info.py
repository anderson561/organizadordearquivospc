"""Gera o arquivo de propriedades que o PyInstaller grava no .exe.

Sem isto o executavel aparece no Windows sem nome de produto e sem versao:
clicar com o botao direito > Propriedades > Detalhes mostra tudo em branco.
Num binario nao assinado, que ja provoca o aviso do SmartScreen, essas
propriedades sao o unico sinal que a pessoa tem para conferir a origem antes
de mandar executar.

O conteudo e derivado de src/version.py, entao nao ha um segundo numero de
versao para esquecer de atualizar.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from version import VERSION_TUPLE, __version__  # noqa: E402

MODELO = """VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={tupla},
    prodvers={tupla},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '041604B0',
        [StringStruct('CompanyName', 'anderson561'),
         StringStruct('FileDescription', 'Organizador Avancado de Arquivos'),
         StringStruct('FileVersion', '{versao}'),
         StringStruct('InternalName', 'OrganizadorArquivosGUI'),
         StringStruct('LegalCopyright', 'MIT License - Copyright (c) 2026 anderson561'),
         StringStruct('OriginalFilename', 'OrganizadorArquivosGUI.exe'),
         StringStruct('ProductName', 'Organizador Avancado de Arquivos'),
         StringStruct('ProductVersion', '{versao}')])
    ]),
    VarFileInfo([VarStruct('Translation', [1046, 1200])])
  ]
)
"""

if __name__ == "__main__":
    destino = Path(__file__).parent / "build" / "version_info.txt"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(MODELO.format(tupla=VERSION_TUPLE, versao=__version__), encoding="utf-8")
    print(f"version_info.txt gerado para a versao {__version__}")
