"""
CiteMind AI - Text Chunker
Splits LoadedChunks into smaller chunks suitable for embedding.
"""
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.data.loader import LoadedChunk
from src.utils.config import config


class Chunker:
    """Recursively splits documents into overlapping chunks."""

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )

    def split(self, loaded_chunks: List[LoadedChunk]) -> List[LoadedChunk]:
        """Split each loaded chunk into smaller pieces."""
        result = []
        for lc in loaded_chunks:
            sub_texts = self.splitter.split_text(lc.text)
            for sub in sub_texts:
                result.append(LoadedChunk(sub, source=lc.source, page=lc.page))
        return result