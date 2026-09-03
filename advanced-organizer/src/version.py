"""Versao do produto, declarada em um lugar so.

O numero aparece em tres superficies - o titulo da janela, a linha de comando
(--version) e as propriedades do arquivo .exe no Windows. Manter tres copias
sincronizadas a mao envelhece mal: basta uma passar batido num release para o
usuario nao conseguir dizer qual build esta rodando. Aqui todas leem daqui.
"""

__version__ = "1.6.0"

# Forma exigida pelo Windows nas propriedades do executavel: quatro inteiros.
VERSION_TUPLE = tuple(int(part) for part in __version__.split(".")) + (0,)
