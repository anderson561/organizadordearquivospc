# MoverArquivos – Documentação Completa

---

## 📖 Visão Geral

`MoverArquivos` é um utilitário para Windows, escrito em Python, que organiza arquivos em pastas com base em estratégias de classificação: **título do documento**, metadados de nota fiscal e extensão do arquivo. A interface gráfica é a forma recomendada de uso; a linha de comando atende automação e diagnóstico.

- **Modo Simulação** (padrão) – apenas relata o que seria movido.
- **Modo Real** – executa a movimentação de fato.
- **Modo Relatório** (`--report`) – lista o título detectado e a pasta de destino de cada arquivo, sem mover nada.
- **Interface Gráfica** – `OrganizadorArquivosGUI.exe` abre uma janela com seleção de pasta, análise prévia (que não move nada), progresso, cancelamento e confirmação antes de mover.

O projeto está estruturado como um **pacote Python** (`advanced‑organizer`) contendo a lógica de organização. O PyInstaller empacota **um único executável**, o da interface gráfica (`OrganizadorArquivosGUI.exe`); a linha de comando é usada pelo interpretador.

---

## 🛠️ Instalação

1. **Pré‑requisitos**
   - Python 3.10 ou superior
   - `pip` (gerenciador de pacotes)
   - Windows 10/11 (o executável foi empacotado para Windows)

2. **Instalar dependências**
   ```bash
   cd C:/python/moverarquivos/advanced-organizer
   python -m venv .venv
   .venv\Scripts\activate   # PowerShell: .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Compilar o executável (opcional)**
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed --name OrganizadorArquivosGUI src/gui.py
   ```
   O binário será colocado em `dist/OrganizadorArquivosGUI.exe`. O script
   `build.bat` faz exatamente isso, preferindo o interpretador da venv.

---

## ▶️ Uso

### Executável (interface gráfica)
```bat
dist\OrganizadorArquivosGUI.exe
```
Informe a pasta, clique em **Analisar** (que nunca move nada) e só então em
**Mover arquivos**, que pede confirmação declarando a quantidade.

### Linha de comando
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

### Módulo Python
```python
from advanced_organizer.src.organizer import FileOrganizer

organizer = FileOrganizer(base_path="C:/Users/ANDERSON/Desktop", dry_run=False)
organizer.organize()
```

### Argumentos de linha de comando
| Argumento | Descrição | Valor padrão |
|-----------|-----------|--------------|
| `--path`  | Caminho da pasta a ser organizada. Se omitido, abre o seletor de pasta. | `None` |
| `--real`  | Executa a movimentação real (caso contrário, só simulação). | `False` |
| `--report`| Lista o título detectado e a pasta de destino de cada arquivo, sem mover nada. | `False` |

---

## 🏗️ Arquitetura

```
advanced-organizer/
│
├─ src/
│   ├─ organizer.py      # Core da aplicação (classe FileOrganizer)
│   ├─ strategies.py     # Estratégias (Título do documento, Empresa, Tipo)
│   ├─ document_terms.py # Vocabulário de termos e regras de plural
│   └─ gui.py            # Interface gráfica (tkinter)
│
├─ tests/                # Testes unitários (pytest)
├─ docs/                 # Esta documentação
├─ build.bat             # Empacota a interface gráfica com PyInstaller
└─ dist/                 # Saída do build (OrganizadorArquivosGUI.exe)
```

- **`FileOrganizer`**: gerencia caminhos‑e‑estratégias, itera sobre diretórios e delega a movimentação.
- **`BaseStrategy`** e subclasses (`DocumentTitleStrategy`, `CompanyNameStrategy`, `TypeStrategy`) determinam a sub‑pasta de destino para cada arquivo.
- **`_move_file`**: encapsula a lógica de criação de diretórios, resolução de conflitos e retry com *tenacity*.
- **Logging**: configurado para `INFO` e inclui timestamps no formato ISO‑8601.

---

## 📚 API (Python)

### `FileOrganizer`
```python
class FileOrganizer:
    def __init__(self, base_path: str = r"C:\Users\ANDERSON\Desktop", dry_run: bool = True)
    def organize(self, progress=None, cancel=None) -> Summary
    def classify_all(self, progress=None, cancel=None) -> List[FilePlan]
    def apply_plans(self, plans, progress=None, cancel=None) -> Summary
    def report(self) -> List[FilePlan]
```
- **`base_path`** – diretório raiz a ser organizado.
- **`dry_run`** – se `True`, apenas registra as ações.
- **`classify_all` / `apply_plans`** – decidir e executar são etapas separadas, para a interface poder mostrar a tabela para revisão sem reler os PDFs na hora de mover.

### Estratégias (`strategies.py`)
```python
class BaseStrategy:
    def get_destination_subpath(self, source_path: str) -> Optional[str]
```
- **`DocumentTitleStrategy`** – lê o título do PDF e agrupa por termo, em pastas no plural (`DARFs`, `Relatórios`). Vocabulário em `src/document_terms.py`. As guias de arrecadação se separam por **jurisdição** — `DAMs` (municipal), `DAEs` (estadual) e `DARFs` (federal) — porque as três começam com a frase "Documento de Arrecadação".
- **`CompanyNameStrategy`** – move documentos empresariais para `Notas/`.
- **`TypeStrategy`** – classifica por extensão (PDF, IMG, DOC, etc.) em sub‑pastas apropriadas.

---

## 🤝 Contribuindo

1. Fork o repositório.
2. Crie um branch para sua feature (`git checkout -b minha-feature`).
3. Instale as dependências de desenvolvimento:
   ```bash
   pip install -r requirements-dev.txt  # inclui pytest, coverage, ruff, pyinstaller
   ```
4. Escreva testes e garanta que `pytest` passe.
5. Submeta um Pull Request com descrição clara e changelog.

---

## 📄 Changelog

| Versão | Data | Alterações |
|--------|------|------------|
| 1.0.0  | 2026‑06‑01 | Lançamento inicial – organização por tipo, UI de seleção de pasta, modo simulação/real. |
| 1.1.0  | 2026-06-03 | Integração de `ruff` como linter, relatório de cobertura, script de verificação automatizado. |
| 1.2.0  | 2026-08-20 | Classificação por título do documento com vocabulário extensível e plural do português. Remoção da `ImpostoStrategy`, que casava `DAS` por substring. Correção de dois bugs de perda de arquivos. |
| 1.3.0  | 2026-08-20 | Interface gráfica em tkinter: análise em duas etapas, progresso, cancelamento e confirmação antes de mover. |
| 1.4.0  | 2026-08-21 | Guias de arrecadação separadas por jurisdição (`DAMs`, `DAEs`, `DARFs`). Limpeza do ruído `(cid:N)` de PDFs sem mapa ToUnicode. |
| 1.4.1  | 2026-08-21 | Empacotamento apenas da interface gráfica; atalhos `.bat` de console removidos. |

---

## 📞 Contato

- **Autor**: Anderson 561 (GitHub: `anderson561`)
- **Contato e issues**: abra tickets em <https://github.com/anderson561/moverarquivos/issues>

---

*Documentação revisada em 2026-08-21.*
