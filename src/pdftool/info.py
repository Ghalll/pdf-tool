from pathlib import Path
from .utils import has_javascript, get_attachments, count_images, get_fonts

"""
def pdf_info(path: Path):
    from pypdf import PdfReader

    try:

        reader = PdfReader(str(path))
        meta   = reader.metadata
        size   = path.stat().st_size / 1024

        print(f"File    : {path.name}")
        print(f"Pages   : {len(reader.pages)}")
        print(f"Size    : {size:.1f} KB  ({size / 1024:.2f} MB)")
        if meta:
            if meta.title:  print(f"Title   : {meta.title}")
            if meta.author: print(f"Author  : {meta.author}")

    except Exception as e:
        print(f"\n[ERROR] Gagal baca info PDF: {e}")
"""

def jpg_info(path: Path):
    from PIL import Image

    try:

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

    except Exception as e:
        print(f"\n [ERROR] Gagal baca indo JPG: {e}")

def doc_info(path: Path, origin: Path | None = None):
    from docx import Document

    origin = origin or path

    try:
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

    except Exception as e:
        print(f"\n[ERROR] Gagal baca info DOC: {e}")

def pdf_analysis(path: Path):
    from pypdf import PdfReader

    try:
        reader  = PdfReader(str(path))
        meta = reader.metadata
        size_kb = path.stat().st_size / 1024
        size_mb = size_kb / 1024
        
        javascript = has_javascript(reader)
        attachments = get_attachments(reader)
        fonts = get_fonts(reader)
        images = count_images(reader)

        print(f"File        : {path.name}")
        print(f"Size        : {size_kb:.1f} KB ({size_mb:.2f}) MB")
        print(f"Pages       : {len(reader.pages)}")
        print(f"Encrypted   : {'Yes' if reader.is_encrypted else 'No'}")
        print(f"JavaScript  : {'Yes' if javascript else 'No'}")
        print(f"Attachments : {len(attachments)}")
        print(f"Images      : {images}")
        print(f"Fonts       : {len(fonts)}")

        print("\nMetadata:")
        if meta:
            print(f"  Title     : {meta.title or '-'}")
            print(f"  Author    : {meta.author or '-'}")
            print(f"  Subject   : {meta.subject or '-'}")
            print(f"  Creator   : {meta.creator or '-'}")
            print(f"  Producer  : {meta.producer or '-'}")
        else:
            print("  None")

        if fonts:
            print("\nFonts:")

            for font in sorted(fonts):
                print(f"  - {font}")

    except Exception as e:
        print(f"\n[ERROR] Gagal analys file PDF: {e}")