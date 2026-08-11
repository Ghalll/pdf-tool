from pathlib import Path


def pdf_info(path: Path):
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    meta   = reader.metadata
    size   = path.stat().st_size / 1024

    print(f"File    : {path.name}")
    print(f"Pages   : {len(reader.pages)}")
    print(f"Size    : {size:.1f} KB  ({size / 1024:.2f} MB)")
    if meta:
        if meta.title:  print(f"Title   : {meta.title}")
        if meta.author: print(f"Author  : {meta.author}")


def jpg_info(path: Path):
    from PIL import Image

    size = path.stat().st_size / 1024
    img  = Image.open(path)

    print(f"File    : {path.name}")
    print(f"Size    : {size:.1f} KB  ({size / 1024:.2f} MB)")
    print(f"Dimensi : {img.width} x {img.height} px")
    print(f"Format  : {img.format}")
    print(f"Mode    : {img.mode}")

    exif = img.getexif()
    if exif:
        print(f"EXIF    : {len(exif)} tag found")

    img.close()


def doc_info(path: Path):
    from docx import Document

    doc    = Document(str(path))
    meta   = doc.core_properties
    size   = path.stat().st_size / 1024
    n_word = sum(len(p.text.split()) for p in doc.paragraphs)

    print(f"File       : {path.name}")
    print(f"Size       : {size:.1f} KB  ({size / 1024:.2f} MB)")
    print(f"Paragraphs : {len(doc.paragraphs)}")
    print(f"Words      : {n_word}")
    if meta.title:  print(f"Title      : {meta.title}")
    if meta.author: print(f"Author     : {meta.author}")