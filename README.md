# 📁 MoverArquivos - advanced-organizer

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-13%20passed-green.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-93%25-green.svg)]()

Um sistema inteligente e resiliente desenvolvido em Python para a organização automatizada e estruturada de diretórios, com foco no Desktop e pastas customizadas do usuário. O projeto lê extensões de arquivos, analisa o conteúdo textual de arquivos PDF para classificar guias de impostos e realiza parsing de metadados complexos em Notas Fiscais eletrônicas.

---

## 🚀 Como Funciona a Organização?

O software adota o padrão de projeto **Strategy** para desacoplar e aplicar regras específicas de organização:

1. **Documentos de Notas Fiscais (`CompanyNameStrategy`):**
   * Processa arquivos PDF no diretório `Notas/`.
   * Realiza extração do texto interno e busca padrões de data e Razão Social do emitente.
   * Cria uma estrutura organizada e limpa de diretórios: `[Ano] / [Mês] / [Nome_da_Empresa]`.

2. **Guias de Impostos (`ImpostoStrategy`):**
   * Processa arquivos PDF no diretório `Impostos/`.
   * Busca palavras-chave internas como `DARF`, `DAS`, `IPTU`, `IPVA` ou `GRERJ`.
   * Move os arquivos para suas respectivas pastas correspondentes aos tributos encontrados.

3. **Arquivos Gerais (`TypeStrategy`):**
   * Processa todos os arquivos na raiz do diretório principal.
   * Organiza os arquivos de acordo com a extensão (ex: `.jpg` vai para a pasta `JPG`, `.xlsx` para `XLSX`).

---

## 🏛️ Arquitetura e Robustez

O projeto foi construído seguindo os melhores padrões de engenharia de software:
* **SOLID Principles:** Baixo acoplamento e alta coesão em todas as classes de estratégias.
* **Resiliência com Retries:** Utiliza a biblioteca `tenacity` para realizar tentativas de escrita com atraso exponencial (exponential backoff) caso ocorra alguma trava no sistema de arquivos do Windows.
* **Prevenção contra Perda de Dados:** Se um arquivo no destino já existir, o novo recebe um sufixo com o timestamp de modificação (`mtime`) e, se esse nome também estiver ocupado, um contador incremental. O destino final é sempre verificado antes do move — a movimentação é abortada em vez de sobrescrever.
* **Resolução de Bloqueios:** Identifica se há um arquivo com o mesmo nome de uma pasta que precisa ser criada e o move para quarentena (`_CONFLITO_F_P`, com contador se o nome já estiver em uso) para liberar a execução sem interrupções.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.13+**
* **pdfminer.six** - Leitura e extração robusta de PDFs.
* **tenacity** - Políticas de retries automáticos.
* **pytest** - Framework de testes unitários.
* **PyInstaller** - Geração de executável binário (`.exe`) independente.

---

## 📦 Estrutura do Repositório

```text
moverarquivos/
├── advanced-organizer/
│   ├── src/
│   │   ├── organizer.py         # Orquestrador e motor de movimentação
│   │   └── strategies.py        # Implementações das regras de negócio
│   ├── tests/
│   │   ├── test_organizer.py    # Testes do fluxo de organização e conflitos
│   │   ├── test_strategies.py   # Testes unitários das estratégias
│   │   └── test_regressions.py  # Regressões de perda de dados (filesystem real)
│   ├── dist/
│   │   └── OrganizadorArquivos.exe  # Executável compilado
│   ├── README.md                # Documentação interna do módulo
│   ├── executar_simulacao.bat   # Execução em modo Dry Run interativo
│   └── executar_real.bat        # Execução real interativa
├── reports/
│   └── verification_report.md   # Saída de verify_project.py
├── requirements.txt             # Dependências de execução (fixadas)
├── requirements-dev.txt         # Testes, lint e empacotamento
├── verify_project.py            # Testes + cobertura + lint + smoke test
└── README.md                    # Este arquivo (Portal do projeto)
```

---

## 🚦 Executando o Projeto

Você pode rodar a aplicação usando os atalhos interativos `.bat` localizados em `advanced-organizer/` ou via PowerShell:

### Modo Simulação (Sem mover arquivos reais)
```bash
advanced-organizer/dist/OrganizadorArquivos.exe --path "C:\Caminho\Da\Pasta"
```

### Modo Execução Real (Movendo arquivos)
```bash
advanced-organizer/dist/OrganizadorArquivos.exe --path "C:\Caminho\Da\Pasta" --real
```

*Nota: Ao rodar os scripts `.bat`, o terminal abrirá um prompt solicitando que digite a pasta. Se apenas pressionar **Enter**, o sistema assumirá o seu Desktop padrão.*

---

## 🧪 Testes Automatizados

O repositório possui **13 testes**, cobrindo simulação, tratamento de duplicidades,
resolução de conflitos e classificação de PDFs. Cobertura medida: **93% no total**
(`strategies.py` 98%, `organizer.py` 75% — o restante é o bloco CLI/Tkinter).

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

### Verificação completa (testes + cobertura + lint + smoke test do binário)
```bash
.venv\Scripts\python.exe verify_project.py
```
O relatório é gravado em `reports/verification_report.md`. O smoke test roda o
executável sempre em **dry run**, contra uma pasta temporária descartável.
