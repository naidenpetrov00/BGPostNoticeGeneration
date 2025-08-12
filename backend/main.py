import shutil
import tempfile
import zipfile

from readData import read_temp_file
from generateNoticeEnvelopes import generateNotice
from fastapi import File, UploadFile,FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-csv")
async def process_csv(file:UploadFile = File(...)):
    suffix = ".xls" if file.filename.endswith(".xls") else ".xlsx"
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    with open(temp_file.name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file = read_temp_file(temp_file.name)

    notice_pdf_path, envelope_pdf_path,protocol_path = await generateNotice(file,mode="single")

    zip_path = tempfile.NamedTemporaryFile(delete=False, suffix=".zip").name
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(notice_pdf_path, arcname="notices.pdf")
        zipf.write(envelope_pdf_path, arcname="envelopes.pdf")
        zipf.write(protocol_path, arcname="protocol.xlsx")

    return StreamingResponse(
        open(zip_path, "rb"),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=notices_and_envelopes.zip"},
    )
