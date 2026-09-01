# verify_project.py
"""Automated verification script for the Organizador Avancado de Arquivos project.

Features:
- Run unit tests with coverage (coverage report generated).
- Lint source code using ruff.
- Smoke-test the CLI in dry-run mode against a throwaway sandbox.
- Validate build script execution.
- Consolidate results into a Markdown report at `reports/verification_report.md`.
"""
import subprocess
import tempfile
import sys
import os
from pathlib import Path

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent  # project root (c:/python/moverarquivos)
ADV_ORG = BASE_DIR / "advanced-organizer"
REPORTS_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORTS_DIR / "verification_report.md"

# A versao do produto vem de src/version.py: o relatorio precisa dizer qual
# build ele verificou, senao nao serve para conferir um .exe ja publicado.
sys.path.insert(0, str(ADV_ORG / "src"))
from version import __version__ as PRODUCT_VERSION  # noqa: E402


def run_cmd(command, cwd=None, shell=False):
    """Run a shell command, capture output, and return (returncode, stdout, stderr).

    stdin is closed on purpose: build.bat ends with `pause`, which would block
    this script forever waiting for a keypress that never comes. With DEVNULL
    the pause reads EOF and returns immediately.
    """
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=shell,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr

def write_section(title: str, content: str):
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(f"## {title}\n\n```\n{content}\n```\n\n")

def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    # Clear previous report
    REPORT_FILE.write_text(f"# Organizador Avancado de Arquivos {PRODUCT_VERSION} - Verification Report\n\nGenerated on " + __import__("datetime").datetime.now().isoformat() + "\n\n", encoding="utf-8")

    # 1. Run tests with coverage
    print("Running tests with coverage...")
    # Determine a valid working directory for pytest/coverage
    # Determine test directory (advanced-organizer/tests)
    test_dir_path = os.path.abspath(str(ADV_ORG / "tests"))
    if os.path.isdir(test_dir_path):
        test_cwd_path = test_dir_path
    else:
        test_cwd_path = os.path.abspath(str(ADV_ORG))
    print(f"[DEBUG] Using test_cwd: {test_cwd_path}")
    rc, out, err = run_cmd([sys.executable, "-m", "coverage", "run", "-m", "pytest"], cwd=test_cwd_path)
    write_section("Test Execution (pytest)", out + "\n" + err)
    if rc == 0:
        # The .coverage data file lives in the same cwd used by `coverage run`,
        # so the report must run from there - otherwise it finds no data.
        rc_cov, out_cov, err_cov = run_cmd([sys.executable, "-m", "coverage", "report", "-m"], cwd=test_cwd_path)
        write_section("Coverage Report", out_cov + "\n" + err_cov)
    else:
        write_section("Test Execution (pytest)", "Tests failed. Skipping coverage.")

    # 2. Lint with ruff
    print("Running ruff linter...")
    lint_targets = [str(ADV_ORG / "src"), str(ADV_ORG / "tests"), str(Path(__file__).resolve())]
    rc_lint, out_lint, err_lint = run_cmd([sys.executable, "-m", "ruff", "check", *lint_targets])
    write_section("Ruff Linting", out_lint + "\n" + err_lint)

    # 3. Smoke-test the CLI in DRY RUN mode.
    # Never use --real here: a verification script must not move real files.
    # A throwaway sandbox is populated so the run has something to classify.
    # Only the GUI is packaged as an .exe, and a --windowed binary cannot be
    # driven from a console: it prints nothing to stdout and opens a window
    # that would block this script. So the CLI is exercised through the
    # interpreter - which is also how the docs tell you to run it.
    cli_path = ADV_ORG / "src" / "organizer.py"
    print("Smoke-testing CLI (dry run)...")
    with tempfile.TemporaryDirectory(prefix="moverarquivos_verify_") as sandbox:
        for sample in ("relatorio.txt", "foto.jpg", "planilha.xlsx", "sem_extensao"):
            Path(sandbox, sample).write_text("sample", encoding="utf-8")

        rc_bin, out_bin, err_bin = run_cmd(
            [sys.executable, str(cli_path), "--path", sandbox],
            cwd=os.path.abspath(str(ADV_ORG)),
        )
        output = out_bin + "\n" + err_bin

        # The sandbox must be untouched: dry run may not move anything.
        leftovers = sorted(p.name for p in Path(sandbox).iterdir())
        dry_run_lines = [ln for ln in output.splitlines() if "[DRY RUN]" in ln]

        verdict = (
            f"exit code: {rc_bin}\n"
            f"dry-run entries logged: {len(dry_run_lines)} (expected 4)\n"
            f"sandbox after run: {leftovers}\n"
            f"sandbox untouched: {len(leftovers) == 4}\n\n{output}"
        )
    write_section("CLI (dry run smoke test)", verdict)

    # 4. Run build script (build.bat) silently
    build_bat = ADV_ORG / "build.bat"
    if build_bat.is_file():
        print("Running build.bat...")
        rc_build, out_build, err_build = run_cmd(["cmd", "/c", str(build_bat)], cwd=str(ADV_ORG))
        # O build produz um unico executavel: a interface grafica.
        dist_dir = ADV_ORG / "dist"
        gui_exe = dist_dir / "OrganizadorArquivosGUI.exe"
        produced = sorted(f.name for f in dist_dir.glob("*.exe")) if dist_dir.is_dir() else []
        write_section(
            "Build Script Output",
            f"exit code: {rc_build}\n"
            f"version packaged: {PRODUCT_VERSION}\n"
            f"OrganizadorArquivosGUI.exe present: {gui_exe.is_file()}\n"
            f"executables in dist/: {produced}\n\n" + out_build + "\n" + err_build,
        )
    else:
        write_section("Build Script Output", "build.bat not found.")

    print(f"Verification report generated at {REPORT_FILE}")

if __name__ == "__main__":
    main()
