"""
CiteMind AI - Document Loader
Loads PDF, DOCX, TXT files with page-level metadata.
"""
import os
from pathlib import Path
from typing import List, Dict
import pdfplumber
from docx import Document as DocxDocument


class LoadedChunk:
    """Represents a single piece of text from a document with metadata."""
    def __init__(self, text: str, source: str, page: int = 0):
        self.text = text
        self.source = source
        self.page = page

    def to_dict(self) -> Dict:
        return {"text": self.text, "source": self.source, "page": self.page}

    def __repr__(self):
        return f"<LoadedChunk source='{self.source}' page={self.page} len={len(self.text)}>"


class DocumentLoader:
    """Unified loader for PDF, DOCX, TXT files."""

    SUPPORTED_EXT = {".pdf", ".docx", ".txt"}

    def load(self, file_path: str) -> List[LoadedChunk]:
        """Load a single file and return list of LoadedChunks (one per page/section)."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower()
        if ext not in self.SUPPORTED_EXT:
            raise ValueError(f"Unsupported file type: {ext}")

        if ext == ".pdf":
            return self._load_pdf(path)
        elif ext == ".docx":
            return self._load_docx(path)
        elif ext == ".txt":
            return self._load_txt(path)

    def _load_pdf(self, path: Path) -> List[LoadedChunk]:
        chunks = []
        with pdfplumber.open(path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                text = self._clean_text(text)
                if text.strip():
                    chunks.append(LoadedChunk(text, source=path.name, page=page_num))
        return chunks

    def _load_docx(self, path: Path) -> List[LoadedChunk]:
        doc = DocxDocument(path)
        full_text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        full_text = self._clean_text(full_text)
        return [LoadedChunk(full_text, source=path.name, page=1)]

    def _load_txt(self, path: Path) -> List[LoadedChunk]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = self._clean_text(f.read())
        return [LoadedChunk(text, source=path.name, page=1)]

    @staticmethod
    def _clean_text(text: str) -> str:
        """Light cleaning: collapse whitespace, strip."""
        import re
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def load_directory(self, dir_path: str) -> List[LoadedChunk]:
        """Load all supported files in a directory."""
        all_chunks = []
        for file in Path(dir_path).iterdir():
            if file.suffix.lower() in self.SUPPORTED_EXT:
                try:
                    all_chunks.extend(self.load(str(file)))
                    print(f"  ✅ Loaded {file.name}")
                except Exception as e:
                    print(f"  ❌ Failed {file.name}: {e}")
        return all_chunks