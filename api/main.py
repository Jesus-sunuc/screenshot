from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
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

@app.post("/process-screenshot")
async def process_screenshot(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    upload_path = None

    try:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")

        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}:
            raise HTTPException(status_code=400, detail="Unsupported image format")

        upload_path = UPLOAD_DIR / f"{file_id}{file_extension}"
        upload_path.write_bytes(await file.read())
        logger.info(f"Uploaded: {upload_path}")

        output_path = OUTPUT_DIR / f"{file_id}.docx"
        processor.process_image(str(upload_path), str(output_path))
        logger.info(f"Generated: {output_path}")

        return {
            "success": True,
            "file_id": file_id,
            "download_url": f"/download/{file_id}"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process screenshot: {str(e)}")
    finally:
        if upload_path and upload_path.exists():
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
