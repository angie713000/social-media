#!/usr/bin/env python3
"""Regenera contenidos-por-marca.html a partir de los scripts de src/.

Uso:  python3 build_all.py
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

for script in ("build_calendario.py", "build_kg_publicaciones.py", "build_unificado.py"):
    print("->", script)
    subprocess.run([sys.executable, script], cwd=SRC, check=True)

shutil.copy(os.path.join(SRC, "contenidos-por-marca.html"), os.path.join(ROOT, "contenidos-por-marca.html"))
print("listo: contenidos-por-marca.html")
