import subprocess
from pathlib import Path
from .utils import run_libreoffice_convert


def pdf_to_jpg(path: Path, dpi: int = 150, quality: int = 85,
               output_dir: Path = None):
    from pdf2image import convert_from_path

    if output_dir is None:
        output_dir = path.parent

    print(f"\n[*] Convert PDF → JPG  |  DPI: {dpi}  |  Quality: {quality}%")

    try:
        images = convert_from_path(str(path), dpi=dpi)
        for i, img in enumerate(images):
            out = output_dir / f"{path.stem}_{i + 1:03d}.jpg"
            img.convert("RGB").save(str(out), "JPEG", quality=quality, optimize=True)
            print(f"[+] Page {i + 1:>3} → {out.name}  ({out.stat().st_size / 1024:.0f} KB)")

        print(f"\n[✓] {len(images)} file saved in: {output_dir.resolve()}")

    except Exception as e:
        print(f"\n[ERROR] Failed to convert: {e}")
        if any(k in str(e).lower() for k in ["poppler", "pdftoppm", "pdfinfo"]):
            print("\n[!] Poppler belum terinstall.")
            print("    Ubuntu/Debian : sudo apt install poppler-utils")
            print("    macOS         : brew install poppler")
            print("    Windows       : https://github.com/oschwartz10612/poppler-windows/releases")


def pdf_to_doc(path: Path, output_path: Path = None):
    from pdf2docx import Converter

    if output_path is None:
        output_path = path.parent / f"{path.stem}.docx"

    print(f"\n[*] Convert PDF → DOCX")

    try:
        cv = Converter(str(path))
        cv.convert(str(output_path))
        cv.close()

        size_kb = output_path.stat().st_size / 1024
        print(f"\n[✓] Converted: {output_path.name}  ({size_kb:.0f} KB)")
        print(f"    Saved in : {output_path.resolve()}")

    except Exception as e:
        print(f"\n[ERROR] Failed to convert: {e}")

def pdf_to_text(path: Path, output_path: Path = None):
    from pypdf import PdfReader

    if output_path is None:
        output_path = path.parent / f"{path.stem}.txt"

    print(f"\n[*] Convert PDF → Text")

    try:
        reader = PdfReader(str(path))
        total = len(reader.pages)
 
        parts = []
        empty_pages = 0
        for page in reader.pages:
            text = page.extract_text() or ""
            if not text.strip():
                empty_pages += 1
            parts.append(text)

        full_text = "\n\n".join(parts)
        output_path.write_text(full_text, encoding="utf-8")
 
        size_kb = output_path.stat().st_size / 1024
        print(f"\n[✓] Converted: {output_path.name}  ({size_kb:.1f} KB)")
        print(f"    Saved in : {output_path.resolve()}")

        if empty_pages:
            print(f"\n    [!] {empty_pages}/{total} halaman nggak ada teks yang bisa diekstrak.")
            print("        Kemungkinan hasil scan/gambar — butuh OCR, bukan text extraction biasa.")

    except Exception as e:
        print(f"\n[ERROR] Failed to convert: {e}")


def jpg_to_pdf(path: Path, output_path: Path = None):
    from PIL import Image

    if output_path is None:
        output_path = path.parent / f"{path.stem}.pdf"

    print(f"\n[*] Convert JPG → PDF")

    try:
        img = Image.open(path).convert("RGB")
        img.save(str(output_path), "PDF", resolution=150.0)
        img.close()

        size_kb = output_path.stat().st_size / 1024
        print(f"\n[✓] Converted: {output_path.name}  ({size_kb:.0f} KB)")
        print(f"    Saved in : {output_path.resolve()}")

    except Exception as e:
        print(f"\n[ERROR] Failed to convert: {e}")


def doc_to_pdf(path: Path, output_dir: Path = None):
    if output_dir is None:
        output_dir = path.parent

    print(f"\n[*] Convert DOCX → PDF")
    print("    (bisa makan waktu lebih lama untuk file besar/kompleks, tunggu sebentar)")

    try:
        result = run_libreoffice_convert(path, "pdf", output_dir)

        output_path = output_dir / f"{path.stem}.pdf"

        if result.returncode != 0 or not output_path.exists():
            print(f"\n[ERROR] Gagal convert: {result.stderr}")
            return

        size_kb = output_path.stat().st_size / 1024
        print(f"\n[✓] Converted: {output_path.name}  ({size_kb:.0f} KB)")
        print(f"    Saved in : {output_path.resolve()}")

    except FileNotFoundError:
        print("\n[ERROR] LibreOffice belum terinstall.")
        print("    Ubuntu/Debian : sudo apt install libreoffice")
        print("    Windows       : https://www.libreoffice.org/download/download/")

    except subprocess.TimeoutExpired:
        print("\n[ERROR] Conversion timeout (file terlalu besar/kompleks).")

    except Exception as e:
        print(f"\n[ERROR] Failed to convert: {e}")