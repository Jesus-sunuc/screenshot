# Screenshot to Word Document Converter

A Python-based application that extracts text from screenshots and converts them into Word documents while preserving formatting, font sizes, and layout structure.

## Features

- **OCR Processing**: Uses Tesseract OCR to extract text from images
- **Format Preservation**: Maintains font sizes, headings, and spacing
- **Docker Support**: Easy deployment with Docker Compose
- **Modern UI**: React frontend with file upload interface
- **FastAPI Backend**: Fast and efficient API for processing

## Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI (Python)
- **OCR Engine**: Tesseract OCR
- **Document Generation**: python-docx

## Prerequisites

- Docker and Docker Compose
- OR:
  - Python 3.11+
  - Node.js 20+
  - Tesseract OCR

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   cd screenshot_docs
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:5173
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Manual Setup (Without Docker)

### Backend Setup

1. **Navigate to API directory**
   ```bash
   cd api
   ```

2. **Activate virtual environment**
   ```bash
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**
   - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

5. **Run the API**
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Navigate to client directory**
   ```bash
   cd client
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Run development server**
   ```bash
   pnpm run dev
   ```

## Usage

1. Open the web interface at http://localhost:5173
2. Click "Choose Image" to select a screenshot
3. Click "Convert to Word" to process the image
4. Download the generated Word document

## How It Works

1. **Image Upload**: User uploads a screenshot through the React frontend
2. **OCR Processing**: Backend uses Tesseract to extract text with layout information
3. **Format Analysis**: Algorithm analyzes font sizes and spacing to determine heading levels
4. **Document Generation**: Creates a Word document with python-docx, preserving the structure
5. **Download**: User downloads the formatted Word document

## API Endpoints

- `GET /` - Health check
- `POST /process-screenshot` - Upload and process screenshot
- `GET /download/{file_id}` - Download generated Word document

## Project Structure

```
screenshot_docs/
├── api/
│   ├── main.py                 # FastAPI application
│   ├── screenshot_processor.py # OCR and document generation logic
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile
├── client/
│   ├── src/
│   │   ├── App.tsx            # Main React component
│   │   └── App.css            # Styling
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## Environment Variables

Create a `.env` file in the client directory:

```env
VITE_API_URL=http://localhost:8000
```

## Limitations

- Images are not preserved in the output document (text only)
- OCR accuracy depends on image quality and clarity
- Complex layouts may require manual adjustment

## Future Enhancements

- [ ] Support for multiple image formats
- [ ] Batch processing
- [ ] Image preservation in output
- [ ] Custom styling templates
- [ ] PDF output option
- [ ] Advanced layout detection

## License

MIT
