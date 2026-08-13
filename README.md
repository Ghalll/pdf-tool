# PDFtool

CLI tool untuk convert dan compress file PDF, JPG, DOC/DOCX langsung dari terminal.

## Kenapa pakai ini?

Layanan online seperti iLovePDF, SmallPDF, dll mengharuskan kamu **upload dokumen ke server pihak ketiga** untuk diproses. Untuk dokumen sensitif (KTP, SIM, ijazah, akta, dll), ini risiko privasi yang nggak perlu — kamu nggak tahu data itu disimpan di mana, berapa lama, dan siapa yang bisa akses.

PDFtool memproses semua file **100% di komputer kamu sendiri**. Tidak ada upload, tidak ada server, tidak ada koneksi internet yang dibutuhkan saat memproses file. Dokumen kamu tidak pernah meninggalkan perangkat kamu.

## Fitur

- **Info file** — cek metadata PDF, JPG, DOCX
- **Convert file** — PDF ↔ JPG, PDF ↔ DOCX
- **Compress file** — kompres PDF, JPG, DOCX dengan level low/medium/high
- **Privacy file** — Membersihkan metadata PDF, JPG. Mengenkripsi file PDF.

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
- GitHub: @GhalyRisyadi
- Email: vrenty882@hotmail.com
- Instagram : @ghalyrisydi

## Lisensi

MIT
