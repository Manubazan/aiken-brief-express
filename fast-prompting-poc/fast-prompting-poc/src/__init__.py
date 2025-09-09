# === SETUP (correr PRIMERO) ===
from pathlib import Path
import sys

ROOT = Path.cwd()
if ROOT.name == "notebooks":   # si la notebook está dentro de /notebooks
    ROOT = ROOT.parent         # sube a la raíz del proyecto

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("ROOT =", ROOT)
print("src existe:", (ROOT / "src").exists())
print("data existe:", (ROOT / "data").exists())
print("src contiene:", [p.name for p in (ROOT / "src").glob("*")])
