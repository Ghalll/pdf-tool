from pathlib import Path

from .utils import clear, input_file, input_files, ensure_docx
from .info import pdf_info, jpg_info, doc_info
from .convert import pdf_to_jpg, pdf_to_doc, jpg_to_pdf, doc_to_pdf
from .compress import pdf_compres, jpg_compres, doc_compres
from .merge_split import merge_pdf, split_pdf, merge_docx, split_docx
from .privacy import pdf_strip_metadata, jpg_strip_exif, pdf_encrypt
from .sanitize import pdf_sanitize


def welcome():
    clear()
    print("\n" + "=" * 40)
    print("\t  I Hate PDF file")
    print("=" * 40)
    print("1\t→\tInfo File")
    print("2\t→\tConvert File")
    print("3\t→\tCompress File")
    print("4\t→\tMerge / Split file")
    print("5\t→\tPrivacy")
    print("\nQ → Quit")

def flow_info_file():
    while True:
        clear()
        print("\nPilih tipe file\n")
        print("1\tPDF")
        print("2\tJPG")
        print("3\tDOC/DOCX")
        print("\n0\tBack")

        choice = input("\nInput [1-3/0] : ").strip()

        if choice == "0":
            return

        ext_map = {"1": [".pdf"], "2": [".jpg", ".jpeg"], "3": [".doc", ".docx"]}
        label_map = {"1": "PDF", "2": "JPG", "3": "DOC/DOCX"}

        if choice not in ext_map:
            print("\n[!] Pilihan tidak valid.")
            input("\nEnter to continue")
            continue

        path = input_file(label_map[choice], ext_map[choice])
        clear()

        if   choice == "1": pdf_info(path)
        elif choice == "2": jpg_info(path)
        elif choice == "3":
            try:
                with ensure_docx(path) as docx_path:
                    doc_info(docx_path, origin=path)
            except Exception as e:
                print(f"\n[ERROR] {e}")

        input("\nEnter to continue")

def flow_convert_file():
    while True:
        clear()
        print("\nConvert ke format apa?\n")
        print("1\tPDF  → JPG")
        print("2\tPDF  → DOCX")
        print("3\tJPG  → PDF")
        print("4\tDOCX → PDF")
        print("\n0\tBack")

        choice = input("\nInput [1-4/0] : ").strip()

        if choice == "0":
            return

        config = {
            "1": ("PDF",      [".pdf"],          pdf_to_jpg),
            "2": ("PDF",      [".pdf"],          pdf_to_doc),
            "3": ("JPG",      [".jpg", ".jpeg"], jpg_to_pdf),
            "4": ("DOC/DOCX", [".doc", ".docx"], doc_to_pdf),
        }

        if choice not in config:
            print("\n[!] Pilihan tidak valid.")
            input("\nEnter to continue")
            continue

        label, exts, func = config[choice]
        path = input_file(label, exts)
        clear()
        func(path)

        input("\nEnter to continue")

def flow_compres_file():
    while True:
        clear()
        print("\nCompress file apa?\n")
        print("1\tPDF")
        print("2\tJPG")
        print("3\tDOC/DOCX")
        print("\n0\tBack")

        choice = input("\nInput [1-3/0] : ").strip()

        if choice == "0":
            return

        config = {
            "1": ("PDF",      [".pdf"],          pdf_compres),
            "2": ("JPG",      [".jpg", ".jpeg"], jpg_compres),
            "3": ("DOC/DOCX", [".doc", ".docx"], doc_compres),
        }

        if choice not in config:
            print("\n[!] Pilihan tidak valid.")
            input("\nEnter to continue")
            continue

        label, exts, func = config[choice]
        path = input_file(label, exts)
        clear()

        if choice == "1": pdf_compres(path)
        elif choice == "2": jpg_compres(path)
        elif choice == "3":
            try:
                with ensure_docx(path) as docx_path:
                    doc_compres(docx_path, origin=path)
            except Exception as e:
                print(f"\n[ERROR] {e}")

        input("\nEnter to continue")

def flow_merge_and_split():
    while True:
        clear()
        print("\n")
        print("1\tMerge PDF")
        print("2\tSplit PDF")
        print("3\tMerge DOCX")
        print("4\tSplit DOCX")
        print("\n0\tBack")

        choice = input("\nInput [1-4/0] : ").strip()

        if choice == "0":
            return

        config = {
            "1": ("PDF",  [".pdf"],          True,  merge_pdf),
            "2": ("PDF",  [".pdf"],          False, split_pdf),
            "3": ("DOCX", [".docx"],         True,  merge_docx),
            "4": ("DOCX", [".docx"],         False, split_docx),
        }

        if choice not in config:
            print("\n[!] Pilihan tidak valid.")
            input("\nEnter to continue")
            continue
        
        label, exts, is_merge, func = config[choice]    

        if is_merge:
            paths = input_files(label, exts)
            clear()
            func(paths)
        else:
            path = input_file(label, exts)
            clear()
            func(path)
            
        input("\nEnter to continue")    


def flow_privacy():
    while True:
        clear()
        print("\nPrivacy — pilih aksi\n")
        print("1\tStrip Metadata  PDF")
        print("2\tStrip EXIF      JPG")
        print("3\tEnkripsi PDF    (password protect)")
        print("4\tSanitize PDF    (strip JS/actions/embedded files)")
        print("\n0\tBack")

        choice = input("\nInput [1-4/0] : ").strip()

        if choice == "0":
            return

        config = {
            "1": ("PDF", [".pdf"],          pdf_strip_metadata),
            "2": ("JPG", [".jpg", ".jpeg"], jpg_strip_exif),
            "3": ("PDF", [".pdf"],          pdf_encrypt),
            "4": ("PDF", [".pdf"],          pdf_sanitize),
        }

        if choice not in config:
            print("\n[!] Pilihan tidak valid.")
            input("\nEnter to continue")
            continue

        label, exts, func = config[choice]
        path = input_file(label, exts)
        clear()
        func(path)
        input("\nEnter to continue")


def main():
    while True:
        welcome()
        opsi = input("\nInput [1-5/Q] : ").strip().upper()

        if   opsi == "Q": print("\nQuit"); break
        elif opsi == "1": flow_info_file()
        elif opsi == "2": flow_convert_file()
        elif opsi == "3": flow_compres_file()
        elif opsi == "4": flow_merge_and_split()
        elif opsi == "5": flow_privacy()
        else:
            print("\n[!] Pilihan tidak valid.")
            input("\nEnter to continue")
