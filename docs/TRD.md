# TRD — Organizador Avançado de Arquivos

**Documento de Requisitos Técnicos**

| | |
|---|---|
| Produto | Organizador Avançado de Arquivos |
| Repositório | `github.com/anderson561/organizadordearquivospc` (público) |
| Versão descrita | 1.8.0 |
| Plataforma | Windows 10/11, Python 3.13+ |
| Data | 2026-11-16 |

Este documento registra **o que o sistema precisa garantir** e **como cada garantia é cumprida e verificada**. A explicação de uso e da API fica em [`PROJECT_DOCUMENTATION.md`](PROJECT_DOCUMENTATION.md); o histórico de versões, em [`CHANGELOG.md`](../CHANGELOG.md).

---

## 1. Contexto e problema

Um escritório de contabilidade acumula, nas pastas de download e na Área de Trabalho, centenas de PDFs fiscais: guias federais (DARF), municipais (DAM), estaduais (DAE), do Simples (DAS), notas fiscais, declarações, recibos, extratos. Os nomes de arquivo são inconsistentes e, muitas vezes, o próprio documento não traz a sigla que o identifica — um DARF da Receita diz apenas "Documento de Arrecadação de Receitas Federais".

Separar isso à mão é lento. Separar errado é pior: uma guia municipal arquivada como federal é uma guia que alguém deixa de pagar.

O sistema classifica cada arquivo pelo **título do documento** e o move para uma pasta por categoria, com uma regra que orienta todas as decisões técnicas:

> **Melhor não classificar do que classificar errado.** Arquivo sem termo reconhecido vai para a pasta da extensão (`PDF`), nunca para uma categoria provável.

## 2. Escopo

**Dentro do escopo**
- Classificação de PDFs pelo título e organização dos demais arquivos pela extensão.
- Movimentação dos arquivos para uma estrutura de pastas por categoria, sem perda de dados.
- Interface gráfica empacotada como `.exe` único, e linha de comando pelo interpretador.

**Fora do escopo**
- Leitura do conteúdo para fins fiscais (valores, vencimentos, apuração).
- Integração com sistemas contábeis.

## 3. Usuários e uso

Usuário principal: contador, não desenvolvedor. Usa o executável por **clique duplo**, sobre pastas reais com centenas a milhares de arquivos (a pasta Downloads de referência tinha ~2.000 PDFs).

Consequências técnicas:
- A ferramenta não pode exigir Python instalado → `.exe` único.
- Uma execução não pode parecer que funcionou quando não funcionou → análise e movimentação são etapas visíveis e separadas, e a simulação declara que nada foi movido.
- Um erro de classificação custa caro e é silencioso → classificação conservadora e revisão antes de mover.

## 4. Requisitos funcionais

| ID | Requisito | Onde é cumprido | Verificado por |
|---|---|---|---|
| RF-01 | Classificar PDF pelo **título**: nome do arquivo + metadado `/Title` + primeiras 5 linhas da página 1. Nunca pelo corpo inteiro. | `strategies.extract_title_region`, `DocumentTitleStrategy` | `test_document_title.py` |
| RF-02 | Pasta de destino no **plural do português** (`DARF` → `DARFs`, `relatório` → `Relatórios`), com exceções irregulares e nome explícito quando necessário. | `document_terms.pluralize_pt`, `Term.folder` | `test_document_title.py` |
| RF-03 | Guias de arrecadação separadas por **jurisdição**: `DAMs` (municipal), `DAEs` (estadual), `DARFs` (federal). A frase genérica "documento de arrecadação" não decide sozinha. | `document_terms.TERMS` | `TestGuiasPorJurisdicao` |
| RF-04 | Guia do Simples gerada pelo PGDASD (`PGDASD-DAS-…`) vai para `DASs`; declaração, extrato e recibo do mesmo programa vão para as próprias pastas. | `Term("PGDASD DAS")` | `TestGuiaDoSimplesPeloPGDASD` |
| RF-05 | Arquivo não-PDF, ou PDF sem termo reconhecido, vai para a pasta da extensão em maiúsculas (`JPG`, `PDF`); sem extensão, `Outros`. | `TypeStrategy` | `test_strategies.py` |
| RF-06 | Notas fiscais colocadas em `<base>/Notas` são organizadas em `[Ano]/[MM - Mês]/[Razão Social]`, com a data de emissão e a razão social rotulada. Sem data válida: `Sem Data`; sem rótulo: `Desconhecido`. Nunca um valor inventado. | `CompanyNameStrategy` | `TestCompanyNameConservadora` |
| RF-07 | **Analisar não move nada.** A análise devolve, por arquivo, o título detectado, a pasta de destino e se algum termo foi reconhecido. | `FileOrganizer.classify_all` | `test_classify_all_nao_move_nada` |
| RF-08 | Mover só depois da análise, com confirmação que declara a quantidade de arquivos e o caminho real de destino. | `gui.OrganizerApp._start_move` | `TestJanela` |
| RF-09 | Todas as categorias são criadas dentro de uma única pasta, **`Arquivos Organizados`**, na raiz da pasta escolhida — também para arquivos lidos da subpasta `Notas`. | `ORGANIZED_ROOT_NAME`, `apply_plans` | testes de integração em `test_document_title.py`, `test_gui.py`, `test_regressions.py` (`TestUmUnicoGuardaChuva`) |
| RF-10 | Uma segunda execução não reprocessa o que já foi organizado: `Arquivos Organizados` nunca é lida. | `_subfolders` exclui o guarda-chuva | `test_guarda_chuva_existente_nao_e_relido` |
| RF-11 | Análise com progresso e cancelamento; cancelar interrompe no arquivo seguinte. | `progress`/`cancel` em `classify_all` e `apply_plans` | `test_cancelamento_no_meio_interrompe` |
| RF-12 | Linha de comando: `--report` (classificação sem mover), simulação por padrão, `--real` para mover, `--version`. | `organizer.py` (`__main__`) | smoke test em `verify_project.py` |
| RF-13 | Aviso antes de mover arquivos dentro de pastas de sistema (`Windows`, `Program Files`, `System32`). | `OrganizerApp._is_system_dir` | `test_detecta_pasta_de_sistema` |
| RF-14 | **OCR de PDF escaneado**: com cabeçalho vazio e nome sem termo, a página 1 é lida pelo OCR nativo do Windows (pt-BR). Título exibido com `[OCR]`. OCR indisponível ou com falha não muda nada: o arquivo segue a regra RF-05. | `ocr.ocr_first_page`, `DocumentTitleStrategy.classify` | `TestOcrDePdfEscaneado`, `TestOcrIndisponivel`; `--diagnostico-ocr` no `.exe` |
| RF-15 | **Migração de pastas de versões anteriores**: subpasta da raiz sem subpastas, com nome de categoria do vocabulário ou de extensão (com todos os arquivos daquela extensão), é movida para dentro de `Arquivos Organizados` e removida se ficar vazia. Reclassificação só "para cima". | `_is_legacy_folder`, `_plan_for`, `_remove_emptied_legacy_folders` | `TestDeteccaoDePastaLegada`, `TestMigracaoDeVersoesAnteriores` |
| RF-16 | **Incluir subpastas** (opcional, desligado por padrão): lê subpastas em qualquer profundidade, exceto `Arquivos Organizados`, `Notas`, pastas legadas e ocultas; a tabela mostra a origem. Pasta do usuário nunca é apagada. | `include_subfolders`, checkbox na GUI, `--subpastas` | `TestSubpastas` |

## 5. Requisitos não funcionais

| ID | Requisito | Como é garantido |
|---|---|---|
| RNF-01 | **Nenhuma perda de dados.** Nunca sobrescrever um arquivo existente. | Colisão de nome ganha sufixo com o `mtime` e, se ainda ocupado, contador incremental. O destino é reconferido imediatamente antes do `move`; se existir, a movimentação é abortada com erro. Travado por `test_regressions.py` no filesystem real. |
| RNF-02 | **Classificação conservadora.** Falso positivo é pior que não classificar. | Casamento por limite de palavra. Acrônimos homógrafos de palavras comuns (`DAS` × "das") exigem caixa alta **e** uma frase de corroboração no título. A janela de título é limitada a 5 linhas. |
| RNF-03 | **Resiliência a travas do Windows** (antivírus, indexador, arquivo aberto). | `tenacity`: 3 tentativas com espera exponencial de 2 a 10 s. |
| RNF-04 | **Conflito arquivo × pasta** não interrompe a execução. | Arquivo que ocupa o nome de uma pasta necessária é renomeado para `_CONFLITO_F_P` (com contador, se preciso) antes de criar a pasta. |
| RNF-05 | **Interface responsiva** durante leitura de centenas de PDFs. | Leitura em thread de trabalho; widgets tocados só pela thread principal; comunicação por fila drenada com `root.after` a cada 100 ms. |
| RNF-06 | **Não reler os PDFs** para mover. | `apply_plans` consome os planos da análise; a classificação não é refeita. |
| RNF-07 | **Robustez a PDFs malformados.** | Ruído `(cid:N)` de fontes sem ToUnicode é limpo antes de recortar a janela de título; falha de leitura vira linha "falha na leitura" e o arquivo cai na extensão. |
| RNF-08 | **Distribuição sem dependências.** | PyInstaller `--onefile --windowed`; só a interface é empacotada. O OCR usa o motor que já vem no Windows — nada a instalar. |
| RNF-09 | **Versão rastreável.** | `src/version.py` é a fonte única: título da janela, `--version`, propriedades do `.exe` e cabeçalho do relatório de verificação. |
| RNF-10 | **Builds reproduzíveis.** | Dependências fixadas em `requirements.txt` / `requirements-dev.txt`; `build.bat` prefere o interpretador da venv do projeto. |

## 6. Arquitetura

### 6.1 Componentes

```
gui.py ──────────┐
                 ├──► organizer.FileOrganizer ──► strategies.* ──► document_terms.TERMS
organizer.py CLI ┘         │                          │
                           │                          ├─► pdfminer.six (página 1, /Title)
                           │                          └─► ocr.py (pypdfium2 + Windows.Media.Ocr, só se escaneado)
                           └─► _move_file (tenacity, anti-sobrescrita, conflitos)
version.py ◄── gui, organizer, gerar_version_info, verify_project
```

| Módulo | Responsabilidade |
|---|---|
| `document_terms.py` | Vocabulário (`Term`), normalização sem acento, pluralização, casamento por regex com limite de palavra. Ordem da tupla `TERMS` = precedência. |
| `strategies.py` | Padrão **Strategy**: `DocumentTitleStrategy` (título → termo → pasta, com `TypeStrategy` de reserva), `CompanyNameStrategy`, `TypeStrategy`. Extração da região de título. |
| `organizer.py` | Orquestração: mapa pasta→estratégia, `classify_all` (decide), `apply_plans` (executa), `_move_file`, relatório e CLI. |
| `gui.py` | Janela única tkinter, máquina de estados (`inicial` → `analisando` → `analisado` → `movendo`), fila de eventos entre threads. |
| `ocr.py` | OCR da página 1 de PDF escaneado: rasteriza com pypdfium2 e reconhece com o OCR nativo do Windows (pt-BR). Devolve `[]` em qualquer falha. |
| `version.py` | Número de versão. |

### 6.2 Fluxo de dados

1. `_iter_files` lista os arquivos diretamente dentro de `<base>` e `<base>/Notas`, depois os das pastas legadas (sempre) e, com "Incluir subpastas", os das demais subpastas em qualquer profundidade. `Arquivos Organizados` nunca é lida.
2. Para cada arquivo, a estratégia da pasta produz um `FilePlan(name, path, title, folder, recognized, origin, legacy)`. Nada é tocado no disco. Em PDF sem texto, o OCR preenche o cabeçalho antes do casamento.
3. A interface (ou o `--report`) mostra os planos.
4. `apply_plans` monta o destino `<base>/Arquivos Organizados/<folder>/<name>` — sempre a partir da pasta escolhida, inclusive para arquivos lidos de `Notas`, e chama `_move_file` para cada plano com `folder`.
5. Pastas legadas que ficaram vazias são removidas (`os.rmdir`, que recusa pasta com conteúdo).
6. Ao final, um `Summary(analisados, movidos, falhas)`.

### 6.3 Decisões de projeto

| Decisão | Motivo | Alternativa descartada |
|---|---|---|
| Classificar pela região de título, não pelo texto inteiro | Casar no corpo mandava "Relatório de **Vendas**" para guias do Simples (`DAS` dentro da palavra). | Busca no texto completo (`ImpostoStrategy`, removida na 1.2.0). |
| Nome do arquivo como um dos três sinais do título | DARFs da Receita não trazem a sigla no conteúdo; DAMs de prefeitura costumam ter fonte sem ToUnicode. O nome cobre esses casos. | Só conteúdo. |
| `FilePlan.folder` guarda só a categoria; `Arquivos Organizados` entra só no caminho físico | A tabela e o relatório mostram a categoria; mudar a pasta guarda-chuva não mexe na classificação. | Embutir o guarda-chuva no plano. |
| Analisar e mover separados | O modo simulação silencioso fazia o usuário achar que a ferramenta não funcionava. | Execução direta com `dry_run`. |
| Empacotar só a interface | Um `.exe --windowed` não pode ser usado pelo console; dois executáveis confundiam o usuário. | Dois executáveis (removido na 1.4.1). |

## 7. Qualidade e verificação

| Item | Estado atual |
|---|---|
| Testes automatizados | 122 (pytest), com PDFs gerados em tempo de teste (`tests/pdf_fixtures.py`), não mocks de extração |
| Cobertura | 93% |
| Lint | `ruff`, sem pendências |
| Verificação completa | `verify_project.py`: testes + cobertura + lint + smoke test da CLI em pasta descartável + build; grava `reports/verification_report.md` com a versão empacotada |

**Definição de pronto** para mudanças de classificação:
1. Teste com PDF real gerado pelo fixture.
2. Censo antes/depois sobre os PDFs reais do usuário: a diferença tem que ser só a pretendida. (Na 1.5.0: 1.996 PDFs, 3 mudanças, todas esperadas.)
3. `.exe` reconstruído e conferido (Propriedades → Detalhes mostra a versão).
4. Documentação revisada **inteira** antes do push.

## 8. Limitações conhecidas e dívida técnica

| ID | Item | Impacto | Encaminhamento sugerido |
|---|---|---|---|
| D8 | OCR lê só a página 1, e só o que o motor do Windows reconhece | Escaneado de baixa qualidade, ou sem idioma pt-BR instalado, continua caindo em `PDF` | Aceito: falha de OCR nunca vira classificação errada. |

Decisões tomadas sobre itens antes listados aqui:

| ID | Item | Decisão (1.8.0) |
|---|---|---|
| D1 | `.exe` sem assinatura digital | **Aceito como decisão, não pendência.** Certificado de assinatura é pago e o público é interno; o aviso do SmartScreen está documentado no README. |
| D2 | Varredura não recursiva | Resolvido: opção "Incluir subpastas" (RF-16). |
| D3 | Sem migração de pastas de versões anteriores | Resolvido: migração automática (RF-15). Na Downloads de referência, os 545 arquivos de `PDF/` passam a ser reclassificados — 444 viram `DARFs`. |
| D7 | Sem OCR | Resolvido: OCR nativo do Windows (RF-14). |

## 9. Ambiente e build

| Item | Valor |
|---|---|
| Execução | `pdfminer.six 20251230`, `tenacity 9.1.4`; OCR: `pypdfium2 5.15.2` e pacotes `winrt-*` 3.2.1 (projeções de `Windows.Media.Ocr`) |
| Desenvolvimento | `pytest 9.0.2`, `coverage 7.14.1`, `ruff 0.15.15`, `pyinstaller 6.19.0` |
| Build | `advanced-organizer/build.bat` → `gerar_version_info.py` → PyInstaller `--onefile --windowed --version-file`, com `--collect-all pypdfium2`/`pypdfium2_raw` e `--collect-submodules winrt` para o OCR |
| Saída | `advanced-organizer/dist/OrganizadorArquivosGUI.exe` (~28 MB) |
| Publicação | Release no GitHub com o `.exe` anexado e o SHA-256 nas notas |

## 10. Como estender o vocabulário

Novo tipo de documento = uma linha em `TERMS` (`document_terms.py`), na posição certa de precedência (específicos antes de genéricos), mais um teste com PDF gerado. Use `acronym=True` para siglas e `requires=(...)` quando a sigla também for uma palavra comum. A lista "sem termo reconhecido" do `--report` é a fonte dos candidatos.
