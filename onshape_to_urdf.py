import json
import os
import subprocess
from pathlib import Path

# ---------------- settings ----------------
ASSEMBLY_URL = "https://cad.onshape.com/documents/40542507499ebe743aa72484/w/042465d31da425a7a200336b/e/51e42c711a696dad00281e81"  # link to the assembly tab
OUTPUT_DIR = Path("robot_export")
ROBOT_NAME = "robot"
DRAW_FRAMES = False  # True to keep frame_ parts visible (debug)

ONSHAPE_ACCESS_KEY = os.environ.get("ONSHAPE_ACCESS_KEY", "")
ONSHAPE_SECRET_KEY = os.environ.get("ONSHAPE_SECRET_KEY", "")
# ------------------------------------------

env = os.environ.copy()
env["ONSHAPE_API"] = "https://cad.onshape.com"
env["ONSHAPE_ACCESS_KEY"] = ONSHAPE_ACCESS_KEY
env["ONSHAPE_SECRET_KEY"] = ONSHAPE_SECRET_KEY

for fmt in ["urdf", "mujoco"]:
    folder = OUTPUT_DIR / fmt
    folder.mkdir(parents=True, exist_ok=True)

    config = {
        "url": ASSEMBLY_URL,
        "output_format": fmt,
        "output_filename": ROBOT_NAME,
        "draw_frames": DRAW_FRAMES,
    }
    (folder / "config.json").write_text(json.dumps(config, indent=4))

    print(f"--- exporting {fmt} ---")
    subprocess.run(["onshape-to-robot", str(folder)], env=env, check=True)

print(f"done -> {OUTPUT_DIR.resolve()}")