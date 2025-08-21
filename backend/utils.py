from datetime import date
from pathlib import Path
import subprocess
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
    print(f"Last Number: {number}")

    with open(last_number_log_path, "a") as a:
        a.write(new_line)


JS_DIR = Path(__file__).parent / "js_script"
REGEN_SCRIPT = JS_DIR / "regen-appearances.js"
BATCH_JS = JS_DIR / "regen_appearances_batch.js"


def regenerate_pdf_appearance(pdf_path: str):
    """Run the Node script to rebuild /AP for a single PDF (in place)."""
    full_path = str(Path(pdf_path).resolve())
    try:
        subprocess.run(
            ["node", str(REGEN_SCRIPT), full_path, full_path],
            check=True,
            cwd=str(JS_DIR),
        )
        print(f"Appearance regenerated: {full_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to regenerate {full_path}: {e}")


def regen_appearances_batch(processed_paths: list[str]):
    if processed_paths:
        try:
            subprocess.run(
                ["node", str(BATCH_JS), *processed_paths],
                check=True,
                cwd=str(JS_DIR),
            )
            print(f"Regenerated appearances for {len(processed_paths)} PDFs")
        except subprocess.CalledProcessError as e:
            print(f"Batch regeneration failed: {e}")


# def merge_pdfs(pdf_paths: list[str], out_path: str):
#     if not pdf_paths:
#         return
#     merger = PdfWriter()
#     for p in pdf_paths:
#         merger.append(str(p)) # type: ignore
#     Path(out_path).parent.mkdir(parents=True, exist_ok=True)
#     with open(out_path, "wb") as f:
#         merger.write(f) # type: ignore
#     merger.close() # type: ignore


def merge_pdfs(pdf_paths: list[str], out_path: str):
    if not pdf_paths:
        return
    writer = PdfWriter()

    for i, p in enumerate(pdf_paths):
        reader = PdfReader(p)
        reader.add_form_topname(f"form{i:04d}")
        writer.append(reader)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        writer.write(f)

import os, json, ipaddress
from typing import Dict, List, Tuple, Optional
from fastapi import Request, HTTPException

def parse_office_ips() -> List[Tuple[str, List[ipaddress._BaseNetwork]]]:
    raw = os.getenv("OFFICE_IPS", "").strip()
    if not raw:
        return []
    try:
        conf: Dict[str, List[str]] = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid OFFICE_IPS JSON: {e}")
    offices: List[Tuple[str, List[ipaddress._BaseNetwork]]] = []
    for office, entries in conf.items():
        nets = []
        for item in entries:
            item = item.strip()
            # ip_network handles both IP and CIDR if strict=False
            nets.append(ipaddress.ip_network(item, strict=False))
        offices.append((office, nets))
    return offices  # keep insertion order (first match wins)

TRUST_PROXY = os.getenv("TRUST_PROXY", "false").lower() == "true"

def client_ip(request: Request) -> str:
    """Get real client IP (trust X-Forwarded-For only if behind a known proxy)."""
    if TRUST_PROXY:
        xff = request.headers.get("x-forwarded-for")
        if xff:
            # first IP in the list is the original client
            return xff.split(",")[0].strip()
        xrip = request.headers.get("x-real-ip")
        if xrip:
            return xrip.strip()
    # fallback to socket peer
    return request.client.host if request.client else "0.0.0.0"

def resolve_office_for_ip(ip_str: str) -> Optional[str]:
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return None
    OFFICE_NETWORKS = parse_office_ips()
    for office, nets in OFFICE_NETWORKS:
        for net in nets:
            if ip in net:
                return office
    return None