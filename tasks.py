import subprocess
import sys


def init_tasks():
    for task in sys.argv[1:]:
        if task not in TASKS:
            raise SystemExit(f"Unknown task: {task}")
        TASKS[task]()


def _build():
    subprocess.run([sys.executable, "-m", "compileall", "."], check=True)


def _spotless_apply():
    """Add # fmt: skip or # fmt: off and # fmt: on for multiple lines"""
    subprocess.run([sys.executable, "-m", "ruff", "format", "."], check=True)
    subprocess.run([sys.executable, "-m", "ruff", "check", "--fix", "."], check=True)


TASKS = {"build": _build, "spotlessApply": _spotless_apply}
