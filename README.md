# PDFtool

CLI tool untuk convert dan compress file PDF, JPG, DOC/DOCX langsung dari terminal.

## Fitur

- **Info file** — cek metadata PDF, JPG, DOCX
- **Convert file** — PDF ↔ JPG, PDF ↔ DOCX
- **Compress file** — kompres PDF, JPG, DOCX dengan level low/medium/high

## Requirement sebelum install

Selain Python, dua dependency sistem ini wajib ada:

| Dependency | Fungsi | Linux | Windows |
|---|---|---|---|
| poppler | convert PDF→JPG | `sudo apt install poppler-utils` | [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases) |
| libreoffice | convert DOC→PDF | `sudo apt install libreoffice` | [libreoffice.org](https://www.libreoffice.org/download/download/) |

## Instalasi

```bash
pipx install git+https://github.com/Ghalll/pdf-tool.git
```

atau pakai pip biasa:
```bash
pip install git+https://github.com/Ghalll/pdf-tool.git
```

## Cara pakai

```bash
pdftool
```

Menu interaktif akan muncul, tinggal ikutin instruksinya.

## Developer

**Ghaly Risyadi**
- GitHub: @Ghalll(https://github.com/Ghalll)
- Email: vrenty882@hotmail.com

## Lisensi

MIT