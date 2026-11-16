# 📁 Organizador Avançado de Arquivos

[![Release](https://img.shields.io/badge/release-v1.6.0-blue.svg)](https://github.com/anderson561/organizadordearquivospc/releases/latest)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-95%20passed-green.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-94%25-green.svg)]()

Um sistema resiliente em Python para organização automatizada de diretórios, com interface gráfica. Classifica documentos pelo **título** — lendo o nome do arquivo, os metadados e o cabeçalho do PDF —, faz parsing de metadados de Notas Fiscais eletrônicas e, como reserva, organiza por extensão. Analisar e mover são etapas separadas: nada sai do lugar sem revisão e confirmação.

---

## 🚀 Como Funciona a Organização?

O software adota o padrão de projeto **Strategy** para desacoplar e aplicar regras específicas de organização:

1. **Documentos de Notas Fiscais (`CompanyNameStrategy`):**
   * Processa arquivos PDF no diretório `Notas/`.
   * Realiza extração do texto interno e busca padrões de data e Razão Social do emitente.
   * Cria a estrutura `[Ano] / [MM - Mês] / [Nome da Empresa]`, por exemplo `2026 / 08 - Agosto / MINIMERCADO BOCA DO RIO LTDA`. Sem data legível usa o mês corrente; sem razão social, `Desconhecido`.

2. **Documentos por Título (`DocumentTitleStrategy`):**
   * Procura um termo conhecido na **região de título**, que reúne três sinais: o **nome do arquivo**, o metadado `/Title` e as primeiras linhas da página 1 — nunca o corpo inteiro do documento.
   * Os três sinais se complementam. Um DARF emitido pela Receita não traz a sigla `DARF` em lugar nenhum do conteúdo (o cabeçalho diz "Documento de Arrecadação"), mas o nome do arquivo quase sempre traz; e quando o nome vem com erro de digitação, o conteúdo cobre.
   * A pasta recebe o termo no **plural**, já que agrupa um ou mais documentos: `DARF` → `DARFs`, `relatório` → `Relatórios`, `nota fiscal` → `Notas Fiscais`.
   * As guias de arrecadação se separam por **jurisdição**: `DAMs` (municipal — ISS, TFF), `DAEs` (estadual — Sefaz) e `DARFs` (federal — Receita). As três começam com a frase "Documento de Arrecadação", então tratá-la como termo único mandava as três para `DARFs`; a frase federal precisa vir completa ("de Receitas Federais").
   * A guia do Simples Nacional é reconhecida pelo prefixo do programa emissor (`PGDASD-DAS-…`), porque em parte dos PDFs o bloco do CNPJ empurra o cabeçalho para fora da região de título. Os outros papéis do mesmo programa — declaração, extrato e recibo — vão para as próprias pastas.
   * O vocabulário fica em [`src/document_terms.py`](advanced-organizer/src/document_terms.py) e é extensível: acrescente um termo e a pasta é derivada automaticamente pelas regras de plural do português.
   * PDF sem termo reconhecido cai na organização por extensão — o programa prefere não classificar a classificar errado.

3. **Arquivos Gerais (`TypeStrategy`):**
   * Reserva usada para arquivos não-PDF e para PDFs sem termo reconhecido.
   * Organiza de acordo com a extensão (ex: `.jpg` vai para a pasta `JPG`, `.xlsx` para `XLSX`).

---

## 🏛️ Arquitetura e Robustez

O projeto foi construído seguindo os melhores padrões de engenharia de software:
* **SOLID Principles:** Baixo acoplamento e alta coesão em todas as classes de estratégias.
* **Classificação Conservadora:** O casamento de termos respeita limite de palavra e, em acrônimos ambíguos, exige caixa alta e corroboração. É isso que impede um "Relatório de Vendas" de virar guia do Simples Nacional por causa da substring `DAS`.
* **Resiliência com Retries:** Utiliza a biblioteca `tenacity` para realizar tentativas de escrita com atraso exponencial (exponential backoff) caso ocorra alguma trava no sistema de arquivos do Windows.
* **Prevenção contra Perda de Dados:** Se um arquivo no destino já existir, o novo recebe um sufixo com o timestamp de modificação (`mtime`) e, se esse nome também estiver ocupado, um contador incremental. O destino final é sempre verificado antes do move — a movimentação é abortada em vez de sobrescrever.
* **Resolução de Bloqueios:** Identifica se há um arquivo com o mesmo nome de uma pasta que precisa ser criada e o move para quarentena (`_CONFLITO_F_P`, com contador se o nome já estiver em uso) para liberar a execução sem interrupções.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.13+**
* **pdfminer.six** - Leitura e extração robusta de PDFs.
* **tenacity** - Políticas de retries automáticos.
* **pytest** - Framework de testes unitários.
* **PyInstaller** - Empacota a interface gráfica num `.exe` único e independente. A linha de comando não é empacotada: roda pelo interpretador.

---

## 📦 Estrutura do Repositório

```text
moverarquivos/
├── advanced-organizer/
│   ├── src/
│   │   ├── organizer.py         # Orquestrador e motor de movimentação
│   │   ├── gui.py               # Interface gráfica (tkinter)
│   │   ├── strategies.py        # Implementações das regras de negócio
│   │   ├── document_terms.py    # Vocabulário de termos e regras de plural
│   │   └── version.py           # Número de versão do produto (fonte única)
│   ├── tests/
│   │   ├── test_organizer.py    # Testes do fluxo de organização e conflitos
│   │   ├── test_strategies.py   # Testes unitários das estratégias
│   │   ├── test_document_title.py  # Classificação por título (PDFs reais)
│   │   ├── test_gui.py          # Interface: dados, estados e fluxo completo
│   │   ├── test_regressions.py  # Regressões de perda de dados (filesystem real)
│   │   └── pdf_fixtures.py      # Gerador mínimo de PDF para os testes
│   ├── dist/
│   │   └── OrganizadorArquivosGUI.exe  # Único executável gerado
│   ├── build.bat                # Empacota a interface gráfica
│   ├── gerar_version_info.py    # Propriedades gravadas no .exe
│   └── README.md                # Documentação interna do módulo
├── reports/
│   └── verification_report.md   # Saída de verify_project.py
├── requirements.txt             # Dependências de execução (fixadas)
├── requirements-dev.txt         # Testes, lint e empacotamento
├── CHANGELOG.md                 # Histórico de versões
├── verify_project.py            # Testes + cobertura + lint + smoke test
└── README.md                    # Este arquivo (Portal do projeto)
```

---

## 🚦 Executando o Projeto

O empacotamento gera **um único executável**: a interface gráfica. A linha de comando continua existindo, rodada pelo interpretador.

### Interface Gráfica (recomendado)

Baixe `OrganizadorArquivosGUI.exe` na [página de releases](https://github.com/anderson561/organizadordearquivospc/releases/latest) e clique duas vezes. Não precisa instalar Python nem nada mais.

> O executável não tem assinatura digital, então o Windows mostra o aviso do SmartScreen na primeira execução: **Mais informações → Executar assim mesmo**. Antes disso vale conferir, em **Propriedades → Detalhes**, se o produto é *Organizador Avancado de Arquivos* na versão esperada.

Quem tem o repositório clonado e roda `build.bat` encontra o mesmo arquivo em:

```bash
advanced-organizer/dist/OrganizadorArquivosGUI.exe
```
Abre uma janela onde você informa a pasta (digitando ou pelo botão **Procurar...**),
clica em **Analisar** e vê, arquivo por arquivo, o título detectado e a pasta de
destino. Só depois de revisar é que o botão **Mover arquivos** habilita, e ele
pede confirmação declarando quantos arquivos serão movidos.

O fluxo é de duas etapas de propósito: analisar **nunca** move nada. Isso torna
impossível o mal-entendido de rodar a ferramenta, ver texto passando na tela e
não perceber que nada aconteceu.

Todo arquivo reconhecido vai para dentro de uma única pasta guarda-chuva,
**`Arquivos Organizados`**, criada na raiz da pasta escolhida — e as categorias
(`DARFs`, `Notas Fiscais`, `JPG`...) nascem dentro dela, não soltas na raiz junto
com o que já estava lá.

### Linha de Comando (pelo interpretador)
```bash
# Relatório: mostra a classificação de cada arquivo sem mover nada
.venv\Scripts\python.exe advanced-organizer/src/organizer.py --path "C:\Caminho\Da\Pasta" --report

# Simulação: registra o que seria movido, sem tocar em nada
.venv\Scripts\python.exe advanced-organizer/src/organizer.py --path "C:\Caminho\Da\Pasta"

# Execução real
.venv\Scripts\python.exe advanced-organizer/src/organizer.py --path "C:\Caminho\Da\Pasta" --real
```
O `--report` lista, para cada arquivo, o **título detectado** e a **pasta de destino**,
e agrupa ao final os PDFs sem termo reconhecido — a mesma informação que o botão
**Analisar** mostra em tabela. É o caminho recomendado antes de qualquer `--real`:
você revisa o resultado e usa a lista de não reconhecidos para decidir quais termos
novos valem entrar no vocabulário.

---

## 🧪 Testes Automatizados

O repositório possui **95 testes**, cobrindo simulação, tratamento de duplicidades,
resolução de conflitos, pluralização em português, extração de título e
classificação de PDFs de verdade (gerados em tempo de teste).

Os testes em `test_regressions.py` usam o filesystem real de propósito: eles travam
dois bugs de perda de arquivos que mocks não reproduzem (sobrescrita silenciosa em
colisões repetidas de nome+`mtime`, e a quarentena de conflito não idempotente).

### Preparando o ambiente
```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

### Rodando os testes
```bash
.venv\Scripts\python.exe -m pytest advanced-organizer/tests
```

### Verificação completa (testes + cobertura + lint + smoke test)
```bash
.venv\Scripts\python.exe verify_project.py
```
O relatório é gravado em `reports/verification_report.md`. O smoke test roda a CLI sempre em **dry run**, contra uma pasta temporária descartável, e o relatório declara quais executáveis o build produziu.

