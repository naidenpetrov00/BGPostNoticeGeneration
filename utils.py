from datetime import date
from pypdf import PdfReader, PdfWriter


def create_single_page_pdf(input_path, output_path, page_index=0):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    writer.add_page(reader.pages[page_index])
    with open(output_path, "wb") as f:
        writer.write(f)


def write_to_pdf(writer, output_path):
    with open(output_path, "wb") as f:
        writer.write(f)


def log_the_last_number():
    last_number_path = "./config/last_number.txt"
    last_number_log_path = "./config/last_number_log.txt"
    with open(last_number_path, "r") as f:
        number = f.read().strip()

    today = date.today().isoformat()
    new_line = f"{today}: {number}\n"

    with open(last_number_log_path,'a') as a:
        a.write(new_line)
