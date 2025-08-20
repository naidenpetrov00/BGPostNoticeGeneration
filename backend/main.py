import os
import shutil
import tempfile
import zipfile

from generate import generate_notice
from readData import read_temp_file
from fastapi import File, HTTPException, UploadFile,FastAPI
from fastapi.responses import FileResponse, StreamingResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

STATIC_FOLDER = os.path.join(os.getcwd(), "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")
app.mount("/assets", StaticFiles(directory="public/assets"), name="assets")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# SPA fallback so /anything returns index.html (except /api/*)
@app.get("/", include_in_schema=False)
@app.get("/{full_path:path}", include_in_schema=False)
def spa_fallback(full_path: str = ""):
    index_path = "public/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="UI not built yet")

@app.post("/api/process-csv")
async def process_csv(file:UploadFile = File(...)):
    suffix = ".xls" if file.filename.endswith(".xls") else ".xlsx" # type: ignore
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    with open(temp_file.name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_df = read_temp_file(temp_file.name)

    generate_result = generate_notice(file_df)

    print(f"Generated:{generate_result}")

    zip_filename = f"notices_and_envelopes_{int(os.path.getmtime(temp_file.name))}.zip"
    zip_path = os.path.join(STATIC_FOLDER, zip_filename)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(generate_result.notices_merged, arcname="notices.pdf")
        zipf.write(generate_result.envelopes_merged, arcname="envelopes.pdf")
        zipf.write(generate_result.protocol_excel, arcname="protocol.xlsx")

    print("Zipped")

    download_url = f"/static/{zip_filename}"
    return JSONResponse({"download_url": download_url})
