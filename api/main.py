from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
import uuid
import logging

from screenshot_processor import ScreenshotProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Screenshot to Docs API",
    description="API for converting screenshots to Word documents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("/app/uploads")
OUTPUT_DIR = Path("/app/outputs")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

processor = ScreenshotProcessor()

@app.get("/")
async def root():
    return {"message": "Screenshot to Docs API is running"}

@app.post("/process-screenshots")
async def process_screenshots(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    file_id = str(uuid.uuid4())
    upload_paths = []

    try:
        for file in files:
            if not file.content_type or not file.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail=f"File {file.filename} must be an image")

            if not file.filename:
                raise HTTPException(status_code=400, detail="Filename is required")

            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}:
                raise HTTPException(status_code=400, detail=f"Unsupported format: {file.filename}")

            upload_path = UPLOAD_DIR / f"{file_id}_{len(upload_paths)}{file_extension}"
            upload_path.write_bytes(await file.read())
            upload_paths.append(upload_path)
            logger.info(f"Uploaded: {upload_path}")

        output_path = OUTPUT_DIR / f"{file_id}.docx"
        processor.process_images([str(p) for p in upload_paths], str(output_path))
        logger.info(f"Generated: {output_path}")

        return {
            "success": True,
            "file_id": file_id,
            "processed_count": len(upload_paths),
            "download_url": f"/download/{file_id}"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process screenshots: {str(e)}")
    finally:
        for upload_path in upload_paths:
            if upload_path.exists():
                upload_path.unlink(missing_ok=True)

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    try:
        uuid.UUID(file_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID format")

    file_path = OUTPUT_DIR / f"{file_id}.docx"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=f"extracted_content_{file_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
