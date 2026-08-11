import getpass
from pathlib import Path


# ─── PDF Metadata ────────────────────────────────────────────────────────────

_PDF_DOCINFO_FIELDS = {
    "/Title":        "Title",
    "/Author":       "Author",
    "/Subject":      "Subject",
    "/Keywords":     "Keywords",
    "/Creator":      "Creator",
    "/Producer":     "Producer",
    "/CreationDate": "Created",
    "/ModDate":      "Modified",
}


def _print_pdf_meta(pdf) -> bool:
    """Print PDF docinfo. Returns True jika ada field yang terisi."""
    found = False
    for key, label in _PDF_DOCINFO_FIELDS.items():
        val = pdf.docinfo.get(key)
        if val:
            print(f"  {label:<12}: {str(val)[:80]}")
            found = True
    return found


def pdf_strip_metadata(path: Path):
    import pikepdf

    print(f"\n[*] Scanning metadata: {path.name}\n")

    try:
        with pikepdf.open(str(path)) as pdf:
            has_meta = _print_pdf_meta(pdf)

            if not has_meta:
                print("  Tidak ada metadata ditemukan.")
                return

            print()
            confirm = input("[?] Strip semua metadata di atas? [Y/n] : ").strip().lower()
            if confirm not in ("", "y", "yes"):
                print("\n[!] Dibatalkan.")
                return

            # Hapus docinfo (metadata tradisional PDF)
            # pikepdf docinfo tidak support .clear() — delete per key
            for key in list(pdf.docinfo.keys()):
                del pdf.docinfo[key]

            # Hapus XMP metadata (metadata modern PDF)
            with pdf.open_metadata() as xmp:
                for key in list(xmp.keys()):
                    del xmp[key]

            output = path.parent / f"{path.stem}_clean.pdf"
            pdf.save(str(output))

        _print_size_result(path, output)
        print(f"    Saved in : {output.resolve()}")

    except Exception as e:
        print(f"\n[ERROR] Gagal strip metadata: {e}")


# ─── JPG EXIF ────────────────────────────────────────────────────────────────

# Tag EXIF yang mengandung info sensitif / identifikasi
_SENSITIVE_EXIF_TAGS = {
    271:   "Make",               # Brand kamera/HP
    272:   "Model",              # Model kamera/HP
    306:   "DateTime",
    36867: "DateTimeOriginal",
    36868: "DateTimeDigitized",
    315:   "Artist",
    33432: "Copyright",
    34853: "GPSInfo",            # Koordinat GPS — paling berbahaya
    40091: "XPAuthor",
    40094: "XPKeywords",
    40092: "XPComment",
}


def jpg_strip_exif(path: Path):
    from PIL import Image, ExifTags

    print(f"\n[*] Scanning EXIF: {path.name}\n")

    try:
        img  = Image.open(path)
        exif = img.getexif()

        if not exif:
            print("  Tidak ada EXIF ditemukan.")
            img.close()
            return

        # Tampilkan tag sensitif
        printed = False
        for tag_id, val in exif.items():
            if tag_id in _SENSITIVE_EXIF_TAGS:
                label = _SENSITIVE_EXIF_TAGS[tag_id]
                print(f"  {label:<24}: {str(val)[:70]}")
                printed = True

        if not printed:
            # Ada EXIF tapi bukan yang sensitif — tetap kasih tau
            print(f"  {len(exif)} tag ditemukan (non-sensitive metadata)")

        print()
        confirm = input("[?] Strip semua EXIF? [Y/n] : ").strip().lower()
        if confirm not in ("", "y", "yes"):
            print("\n[!] Dibatalkan.")
            img.close()
            return

        output = path.parent / f"{path.stem}_clean.jpg"

        # Save tanpa pass kwarg `exif` → Pillow tidak include EXIF
        clean = img.convert("RGB")
        clean.save(str(output), "JPEG", quality=95, optimize=True)
        img.close()

        # Verifikasi — pastiin EXIF beneran hilang
        check      = Image.open(output)
        exif_after = check.getexif()
        check.close()

        _print_size_result(path, output)
        if exif_after:
            print(f"    [!] Warning: masih ada {len(exif_after)} tag tersisa (non-critical).")
        else:
            print("    [✓] Verifikasi: EXIF bersih.")
        print(f"    Saved in : {output.resolve()}")

    except Exception as e:
        print(f"\n[ERROR] Gagal strip EXIF: {e}")


# ─── PDF Encrypt ─────────────────────────────────────────────────────────────

def pdf_encrypt(path: Path):
    import pikepdf

    print(f"\n[*] Enkripsi PDF: {path.name}")
    print("    Algoritma : AES-256  (PDF Revision 6)\n")

    try:
        password = getpass.getpass("Password    : ")
        if not password:
            print("\n[!] Password tidak boleh kosong.")
            return

        confirm = getpass.getpass("Konfirmasi  : ")
        if password != confirm:
            print("\n[!] Password tidak cocok.")
            return

        output = path.parent / f"{path.stem}_encrypted.pdf"

        with pikepdf.open(str(path)) as pdf:
            pdf.save(
                str(output),
                encryption=pikepdf.Encryption(
                    owner=password,
                    user=password,
                    R=6,  # AES-256
                )
            )

        size_kb = output.stat().st_size / 1024
        print(f"\n[✓] PDF terenkripsi: {output.name}  ({size_kb:.0f} KB)")
        print(f"    Saved in : {output.resolve()}")
        print("\n    [!] Tidak ada cara recover password — simpan baik-baik.")

    except pikepdf.PasswordError:
        print("\n[ERROR] PDF ini sudah ter-enkripsi. Decrypt dulu sebelum re-enkripsi.")

    except Exception as e:
        print(f"\n[ERROR] Gagal enkripsi: {e}")


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _print_size_result(original: Path, output: Path):
    before_kb = original.stat().st_size / 1024
    after_kb  = output.stat().st_size / 1024
    print(f"\n[✓] Output  : {output.name}")
    print(f"    Before  : {before_kb:.0f} KB")
    print(f"    After   : {after_kb:.0f} KB")
