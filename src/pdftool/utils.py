import os
from pathlib import Path

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def input_file(label: str, extensions: list[str]) -> Path:
    ext_display = "/".join(e.upper() for e in extensions)
    while True:
        raw = input(f"\nPath {label} file [{ext_display}] : ").strip().strip('"').strip("'")
        p = Path(raw)
        if not p.exists():
            print("[!] File not found.")
        elif p.suffix.lower() not in extensions:
            print(f"[!] File harus berekstensi {ext_display}.")
        else:
            return p
