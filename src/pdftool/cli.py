from pathlib import Path

from .utils import clear, input_file
from .info import pdf_info, jpg_info, doc_info
from .convert import pdf_to_jpg, pdf_to_doc, jpg_to_pdf, doc_to_pdf
from .compress import pdf_compres, jpg_compres, doc_compres

def welcome():
    clear()
    print("\n" + "=" * 40)
    print("\t" + "    I hate PDF")
    print("=" * 40)
    print("1\t→\tInfo File")
    print("2\t→\tConvert File")
    print("3\t→\tCompress File")
    print("\nQ → Quit")

def flow_info_file():
    while True:
        clear()
        print("\nChose your file type\n")
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
        elif choice == "3": doc_info(path)
 
        input("\nEnter to continue")

def flow_convert_file():
    while True:
        clear()
        print("\nwhat do you to convert to?\n")
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
            print("\n[!] Option not valid.")
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
        print("\nWhat file do you to compres?\n")
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
            print("\n[!] Option not valid.")
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
        opsi = input("\nInput [1-3/Q] : ").strip().upper()
 
        if   opsi == "Q": print("\nQuit"); break
        elif opsi == "1": flow_info_file()
        elif opsi == "2": flow_convert_file()
        elif opsi == "3": flow_compres_file()
        else:
            print("\n[!] Option not valid.")
            input("\nEnter to continue")
