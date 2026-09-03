# Changelog

Todas as mudanças relevantes do **Organizador Avançado de Arquivos**.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o
projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

As versões até a 1.4.3 existiram apenas no histórico do repositório: a 1.5.0 é a
primeira publicada como release, com executável anexado.

---

## [1.6.0] - 2026-09-03

### Adicionado

- **Pasta guarda-chuva `Arquivos Organizados`.** Ao mover, cada categoria
  (`DARFs`, `Notas Fiscais`, `JPG`...) passa a nascer dentro de uma única pasta
  nova na raiz escolhida, em vez de solta ali junto com o que já existia. Numa
  pasta como a Downloads do usuário, isso troca uma dezena de pastas novas por
  uma só.
- A confirmação da interface gráfica, antes de mover, agora mostra o caminho
  real de destino (com o guarda-chuva incluído), não só a raiz escolhida.

Não migra pastas de execuções anteriores: categorias já criadas direto na raiz
por uma versão anterior continuam onde estão. Só o que for movido a partir
desta versão nasce dentro do guarda-chuva.

## [1.5.0] - 2026-09-01 — primeiro release público

### Adicionado

- Versão única em [`src/version.py`](advanced-organizer/src/version.py), exibida
  no título da janela, na linha de comando (`--version`) e nas propriedades do
  `.exe`. Antes não havia como dizer qual build estava rodando.
- Propriedades de arquivo no executável (nome do produto, versão, copyright),
  geradas no build por `gerar_version_info.py`. Num binário sem assinatura
  digital, é o único sinal de origem que o Windows mostra.
- `CHANGELOG.md` na raiz, substituindo a tabela que vivia dentro da
  documentação técnica.

### Corrigido

- **Guia do Simples Nacional emitida pelo PGDASD ia para a pasta errada.** Em
  parte dos PDFs o bloco do CNPJ vem antes do cabeçalho e empurra a frase
  "Documento de Arrecadação do Simples Nacional" para fora das cinco linhas da
  região de título; sem ela, a corroboração exigida pelo acrônimo `DAS` nunca
  chegava e a guia caía na organização por extensão. O vocabulário passou a
  reconhecer o prefixo do programa emissor (`PGDASD-DAS-…`), que está sempre no
  nome do arquivo. Os outros papéis do mesmo programa — declaração, extrato e
  recibo — continuam indo para as próprias pastas: é o segmento após `PGDASD`
  que decide, não o prefixo.

## [1.4.3] - 2026-08-27

- Repositório renomeado de `moverarquivos` para `organizadordearquivospc`. A
  pasta local e o nome do produto seguem inalterados.

## [1.4.2] - 2026-08-21

- Revisão completa da documentação contra o código: instruções de instalação e
  exemplo de import que não funcionavam, descrições de `CompanyNameStrategy` e
  `TypeStrategy` divergentes do comportamento real, árvore de arquivos
  incorreta.
- A mensagem do modo simulação citava um atalho `.bat` que havia sido removido.

## [1.4.1] - 2026-08-21

- Empacotamento apenas da interface gráfica. Os atalhos `.bat` de console foram
  removidos: chamavam um executável que deixou de ser gerado.

## [1.4.0] - 2026-08-21

- Guias de arrecadação separadas por jurisdição: `DAMs` (municipal), `DAEs`
  (estadual) e `DARFs` (federal). As três começam com "Documento de
  Arrecadação", e tratar a frase como termo único mandava todas para `DARFs` —
  foi assim que um DAM municipal foi arquivado como guia federal.
- Limpeza do ruído `(cid:N)` que PDFs com fonte sem mapa ToUnicode injetam na
  região de título, antes da janela de cinco linhas, para que o ruído não
  esconda um cabeçalho legível.

## [1.3.0] - 2026-08-20

- Interface gráfica em tkinter: análise e movimentação em etapas separadas, com
  progresso, cancelamento e confirmação declarando a quantidade antes de mover.

## [1.2.0] - 2026-08-20

- Classificação pelo título do documento, com vocabulário extensível e regras de
  plural do português.
- Remoção da `ImpostoStrategy`, que casava `DAS` por substring e classificava
  qualquer documento com a palavra "VENDAS" como guia do Simples Nacional.
- Correção de dois bugs de perda de arquivos.

## [1.1.0] - 2026-06-03

- `ruff` como linter, relatório de cobertura e script de verificação
  automatizado.

## [1.0.0] - 2026-06-01

- Lançamento inicial: organização por tipo, seleção de pasta pela interface e
  modo simulação/real.

[1.6.0]: https://github.com/anderson561/organizadordearquivospc/releases/tag/v1.6.0
[1.5.0]: https://github.com/anderson561/organizadordearquivospc/releases/tag/v1.5.0
