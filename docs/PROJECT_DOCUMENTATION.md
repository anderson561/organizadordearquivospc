# Organizador Avançado de Arquivos – Documentação Completa

Versão documentada: **1.7.0**.

---

## 📖 Visão Geral

O **Organizador Avançado de Arquivos** é um utilitário para Windows, escrito em Python, que organiza
arquivos em pastas com base em estratégias de classificação: **título do
documento**, metadados de nota fiscal e extensão do arquivo. A interface gráfica
é a forma recomendada de uso; a linha de comando atende automação e diagnóstico.

- **Interface Gráfica** – `OrganizadorArquivosGUI.exe` abre uma janela com
  seleção de pasta, análise prévia (que não move nada), progresso, cancelamento
  e confirmação antes de mover.
- **Modo Simulação** (padrão na CLI) – apenas registra o que seria movido.
- **Modo Real** (`--real`) – executa a movimentação de fato.
- **Modo Relatório** (`--report`) – lista o título detectado e a pasta de destino
  de cada arquivo, sem mover nada.

O código-fonte vive em `advanced-organizer/src/`. **Não é um pacote importável**:
o diretório tem hífen no nome e não há `__init__.py`, então os módulos são
carregados por caminho (veja *Módulo Python*, abaixo). O PyInstaller empacota
**um único executável**, o da interface gráfica.

---

## 🛠️ Instalação

1. **Pré-requisitos**
   - Python 3.13+ (versão em que o projeto é testado)
   - Windows 10/11 (o executável é empacotado para Windows)

2. **Instalar dependências** — a partir da **raiz do repositório**, onde ficam os
   arquivos de requisitos:
   ```bash
   cd C:/python/moverarquivos
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
   Para desenvolver (testes, lint, empacotamento), use `requirements-dev.txt`,
   que inclui as dependências de execução.

3. **Compilar o executável (opcional)** — a partir de `advanced-organizer/`:
   ```bash
   build.bat
   ```
   O script prefere o interpretador da venv do projeto e gera
   `dist/OrganizadorArquivosGUI.exe`. Equivale a:
   ```bash
   python -m PyInstaller --onefile --windowed --name OrganizadorArquivosGUI src\gui.py
   ```

---

## ▶️ Uso

### Interface gráfica
```bat
dist\OrganizadorArquivosGUI.exe
```
Informe a pasta, clique em **Analisar** (que nunca move nada), revise a tabela
`arquivo → título detectado → pasta` e só então use **Mover arquivos**, que pede
confirmação declarando a quantidade.

O fluxo tem duas etapas de propósito: analisar **nunca** move nada. Isso elimina
pela estrutura o mal-entendido de rodar a ferramenta, ver log passando na tela e
não perceber que nada aconteceu.

### Linha de comando
A partir de `advanced-organizer/`:
```bat
rem Relatório: classificação de cada arquivo, sem mover nada
..\.venv\Scripts\python.exe src\organizer.py --path "C:\pasta" --report

rem Simulação (padrão, sem --real)
..\.venv\Scripts\python.exe src\organizer.py --path "C:\pasta"

rem Execução real
..\.venv\Scripts\python.exe src\organizer.py --path "C:\pasta" --real

rem Sem --path: abre um seletor de pasta
..\.venv\Scripts\python.exe src\organizer.py --real
```

### Argumentos de linha de comando
| Argumento | Descrição | Valor padrão |
|-----------|-----------|--------------|
| `--path`  | Caminho da pasta a ser organizada. Se omitido, abre o seletor de pasta. | `None` |
| `--real`  | Executa a movimentação real (caso contrário, só simulação). | `False` |
| `--report`| Lista o título detectado e a pasta de destino de cada arquivo, sem mover nada. | `False` |
| `--version`| Mostra a versão e sai. | — |

### Módulo Python
Como `advanced-organizer` não é um pacote importável, acrescente `src/` ao
`sys.path` — é o que os testes fazem:
```python
import sys
sys.path.append(r"C:\python\moverarquivos\advanced-organizer\src")

from organizer import FileOrganizer

# Decidir e executar são etapas separadas.
planos = FileOrganizer(base_path=r"C:\pasta\a\organizar", dry_run=True).classify_all()
for p in planos:
    print(p.name, "->", p.folder, "| titulo:", p.title)

# Para mover de verdade, um organizer com dry_run=False.
resumo = FileOrganizer(base_path=r"C:\pasta\a\organizar", dry_run=False).apply_plans(planos)
print(resumo.movidos, "movidos,", resumo.falhas, "falhas")
```

---

## 🏗️ Arquitetura

```
moverarquivos/
│
├─ advanced-organizer/
│   ├─ src/
│   │   ├─ organizer.py      # Core da aplicação (classe FileOrganizer)
│   │   ├─ strategies.py     # Estratégias (Título do documento, Empresa, Tipo)
│   │   ├─ document_terms.py # Vocabulário de termos e regras de plural
│   │   ├─ version.py        # Número de versão (fonte única do produto)
│   │   └─ gui.py            # Interface gráfica (tkinter)
│   ├─ tests/                # Testes (pytest) e gerador de PDF de fixture
│   ├─ build.bat             # Empacota a interface gráfica com PyInstaller
│   ├─ gerar_version_info.py # Propriedades gravadas no .exe (nome, versão)
│   ├─ dist/                 # Saída do build (OrganizadorArquivosGUI.exe)
│   └─ README.md             # Documentação interna do módulo
│
├─ docs/                     # Esta documentação
├─ reports/                  # Saída de verify_project.py
├─ CHANGELOG.md              # Histórico de versões
├─ requirements.txt          # Dependências de execução (fixadas)
├─ requirements-dev.txt      # Testes, lint e empacotamento
└─ verify_project.py         # Testes + cobertura + lint + smoke test + build
```

- **`FileOrganizer`**: mapeia pastas para estratégias, itera sobre os arquivos e
  delega a movimentação.
- **`BaseStrategy`** e subclasses (`DocumentTitleStrategy`, `CompanyNameStrategy`,
  `TypeStrategy`) determinam a subpasta de destino de cada arquivo.
- **`_move_file`**: criação de diretórios, resolução de conflitos, garantia de
  não sobrescrita e retry com *tenacity*.
- **Logging**: nível `INFO`, com data e hora em cada linha.

---

## 📚 API (Python)

### `FileOrganizer`
```python
class FileOrganizer:
    def __init__(self, base_path: str, dry_run: bool = True)
    def classify_all(self, progress=None, cancel=None) -> List[FilePlan]
    def apply_plans(self, plans, progress=None, cancel=None) -> Summary
    def organize(self, progress=None, cancel=None) -> Summary
    def report(self) -> List[FilePlan]
```
- **`base_path`** – diretório raiz a ser organizado. Obrigatório: não há pasta padrão.
- **`dry_run`** – se `True`, apenas registra as ações.
- **`classify_all` / `apply_plans`** – decidir e executar são etapas separadas,
  para a interface mostrar a tabela de revisão sem reler os PDFs na hora de mover.
- **`progress(feitos, total, plano)`** e **`cancel() -> bool`** – ganchos usados
  pela interface para barra de progresso e cancelamento.
- **`FilePlan`** – `(name, path, title, folder, recognized)`. `recognized` é
  `False` quando nenhum termo do vocabulário casou.
- **`Summary`** – `(analisados, movidos, falhas)`.

### Estratégias (`strategies.py`)
```python
class BaseStrategy:
    def get_destination_subpath(self, source_path: str) -> Optional[str]
```
- **`DocumentTitleStrategy`** – procura um termo do vocabulário na região de
  título (nome do arquivo + metadado `/Title` + primeiras linhas da página 1) e
  devolve a pasta no plural (`DARFs`, `Relatórios`). PDF sem termo reconhecido
  cai na `TypeStrategy` de reserva. As guias de arrecadação se separam por
  **jurisdição** — `DAMs` (municipal), `DAEs` (estadual) e `DARFs` (federal) —
  porque as três começam com a frase "Documento de Arrecadação", e a federal
  precisa vir completa ("de Receitas Federais").
- **`CompanyNameStrategy`** – para notas fiscais. Extrai a data e a razão
  social do PDF e devolve o caminho `[Ano]/[MM - Mês]/[Empresa]`, por exemplo
  `2026/08 - Agosto/MINIMERCADO BOCA DO RIO LTDA`. Segue a mesma regra
  conservadora do resto do projeto: prefere a data rotulada como emissão e
  ignora datas impossíveis; sem data válida devolve `Sem Data/[Empresa]`,
  nunca o mês corrente. A razão social vem só de um rótulo (`Razão Social`,
  `Nome/Razão Social`, `Emitente`, com ou sem acento); sem rótulo,
  `Desconhecido` — nunca a primeira linha, que costuma ser "NOTA FISCAL" ou o
  nome da prefeitura. Arquivo não-PDF cai na `TypeStrategy`.
- **`TypeStrategy`** – devolve a extensão em maiúsculas como nome de pasta
  (`.jpg` → `JPG`, `.xlsx` → `XLSX`). Arquivo sem extensão vai para `Outros`.

### Onde cada estratégia é montada
`FileOrganizer` associa cada pasta a uma estratégia:

| Pasta | Estratégia |
|---|---|
| `<base>` | `DocumentTitleStrategy` |
| `<base>/Notas` | `CompanyNameStrategy` |

A varredura **não é recursiva**: só os arquivos diretamente dentro dessas pastas
são considerados.

A subpasta `<base>/Impostos` deixou de ser varrida na 1.7.0: usava a mesma
estratégia que a própria raiz e só produzia um aviso de "caminho não
encontrado" a cada execução.

### Pasta guarda-chuva (`ORGANIZED_ROOT_NAME`)
`apply_plans` não move o arquivo direto para `<base>/<categoria>/`; insere
`Arquivos Organizados` entre os dois: `<base>/Arquivos Organizados/<categoria>/`.
O destino é sempre ancorado na **pasta escolhida** (`<base>`), mesmo para
arquivos lidos de `<base>/Notas` — existe um único
guarda-chuva, na raiz. Isso é o que separa, na pasta escolhida, o que o
programa criou do que já estava lá — em vez de uma dezena de pastas novas
(`DARFs`, `Notas Fiscais`, `JPG`...) nascendo soltas ao lado de tudo que já
existia, nasce uma única pasta nova.

`FilePlan.folder` continua guardando só o nome da categoria (`"DARFs"`), sem o
guarda-chuva — é ele que a tabela da interface e o `--report` mostram. O
guarda-chuva é inserido só no momento de montar o caminho físico de destino,
dentro de `apply_plans`. Como a raiz escaneada é lida com `os.listdir`, não
recursivo, o conteúdo de `Arquivos Organizados` nunca é reprocessado numa
segunda execução.

**Não migra pastas de execuções anteriores.** Categorias já criadas direto na
raiz por uma versão anterior (por exemplo `Downloads/DARFs`) continuam onde
estão; só o que for movido a partir desta versão passa a nascer dentro do
guarda-chuva. Consolidar o que já existe é decisão manual do usuário.

---

## 🔤 Estendendo o vocabulário

Cada entrada de `TERMS` em `src/document_terms.py` declara o termo no singular; o
nome da pasta é derivado pelas regras de plural do português (`certidão` →
`Certidões`, `edital` → `Editais`, `DARF` → `DARFs`).

```python
Term("alvará")                                   # -> Alvarás
Term("DAM", acronym=True)                        # -> DAMs
Term("nota fiscal", folder="Notas Fiscais")      # nome de pasta explícito
Term("DAS", acronym=True, requires=("SIMPLES NACIONAL",))
```

A ordem de `TERMS` é a precedência: o primeiro termo que casar vence, então os
mais específicos vêm antes dos genéricos. `requires` é corroboração obrigatória
para termos ambíguos — sem ela, `DAS` casaria com a preposição "das".

Use `--report` para descobrir quais títulos dos seus documentos ainda não têm
termo: a lista de "sem termo reconhecido" é exatamente o insumo dessa tarefa.

---

## 🧪 Verificação

A partir da raiz do repositório:
```bash
.venv\Scripts\python.exe -m pytest advanced-organizer/tests   # 101 testes
.venv\Scripts\python.exe verify_project.py                    # + cobertura, lint, smoke test e build
```
`verify_project.py` grava `reports/verification_report.md` com testes, cobertura,
lint, smoke test da CLI em dry run e a lista de executáveis que o build produziu.

---

## 🤝 Contribuindo

1. Crie um branch para a mudança (`git checkout -b minha-feature`).
2. Instale as dependências de desenvolvimento a partir da raiz:
   ```bash
   .venv\Scripts\python.exe -m pip install -r requirements-dev.txt
   ```
3. Escreva testes. Mudança de classificação precisa de teste com PDF de verdade —
   use o gerador em `tests/pdf_fixtures.py`.
4. Rode `verify_project.py` e garanta testes e lint limpos.
5. Atualize esta documentação e o [`CHANGELOG.md`](../CHANGELOG.md) na raiz
   **antes** de subir.
6. Ao publicar uma versão, altere `src/version.py` — é dele que saem o título
   da janela, o `--version` e as propriedades do `.exe`.

---

## 📄 Changelog

O histórico de versões vive em [`CHANGELOG.md`](../CHANGELOG.md), na raiz do
repositório. Ele ficava duplicado aqui como tabela; duas listas de versão
divergem na primeira vez que alguém atualiza só uma.

---

## 📞 Contato

- **Autor**: Anderson 561 (GitHub: `anderson561`)
- **Contato e issues**: abra tickets em <https://github.com/anderson561/organizadordearquivospc/issues>

---

*Documentação revisada em 2026-11-16, na preparação da versão 1.7.0.*
