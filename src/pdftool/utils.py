import os
import subprocess
import tempfile
from contextlib import contextmanager
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


@contextmanager
def ensure_docx(path: Path):
    """
    doc_info/doc_compres cuma bisa baca .docx (zip/XML), bukan .doc lawas
    (OLE binary). Kalau input-nya .docx, langsung dipakai apa adanya.
    Kalau .doc, di-convert dulu ke .docx lewat LibreOffice ke temp dir,
    di-yield path hasil konversinya, terus temp dir dihapus otomatis
    begitu selesai dipakai — nggak ninggalin file sisa di komputer user.
    """
    if path.suffix.lower() == ".docx":
        yield path
        return

    print(f"\n[*] '{path.name}' masih format .doc lama — mengonversi ke .docx dulu (via LibreOffice)...")

    with tempfile.TemporaryDirectory(prefix="pdftool_") as tmp:
        tmp_dir = Path(tmp)
        try:
            result = subprocess.run(
                ["libreoffice", "--headless", "--convert-to", "docx",
                 "--outdir", str(tmp_dir), str(path)],
                capture_output=True, text=True, timeout=60
            )
        except FileNotFoundError:
            raise RuntimeError(
                "LibreOffice belum terinstall.\n"
                "    Ubuntu/Debian : sudo apt install libreoffice\n"
                "    Windows       : https://www.libreoffice.org/download/download/"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Konversi .doc → .docx timeout (file terlalu besar/kompleks).")

        converted = tmp_dir / f"{path.stem}.docx"
        if result.returncode != 0 or not converted.exists():
            detail = (result.stderr or "").strip() or "unknown error"
            raise RuntimeError(f"Gagal mengonversi .doc ke .docx: {detail}")

        print("[✓] Konversi selesai.\n")
        yield converted


def input_files(label: str, extensions: list[str], min_files: int = 2) -> list[Path]:
    """Input banyak file berurutan (buat merge). Kosongkan input buat selesai."""
    ext_display = "/".join(e.upper() for e in extensions)
    paths: list[Path] = []

    print(f"\nMasukkan file {label} satu-satu, urutan sesuai input jadi urutan merge.")
    print("Kosongkan input lalu Enter kalau sudah selesai.")

    while True:
        raw = input(f"\nFile #{len(paths) + 1} [{ext_display}] (kosong = selesai) : ").strip().strip('"').strip("'")

        if raw == "":
            if len(paths) < min_files:
                print(f"[!] Minimal {min_files} file untuk merge.")
                continue
            return paths

        p = Path(raw)
        if not p.exists():
            print("[!] File not found.")
        elif p.suffix.lower() not in extensions:
            print(f"[!] File harus berekstensi {ext_display}.")
        elif p in paths:
            print("[!] File sudah ditambahkan.")
        else:
            paths.append(p)
            print(f"    [+] {len(paths)}. {p.name}")