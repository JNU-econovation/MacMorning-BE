from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class VectorConfig:
    chroma_host: str = os.getenv("CHROMA_HOST")
    chroma_port: int = os.getenv("CHROMA_PORT")
    chroma_collection_name: str = "story_chunks"
    chroma_persist_directory: str = os.getenv("./chroma_db")
    
    embedding_model_name: str = "text-embedding-3-small"
    openai_api_key: Optional[str] = None
    
    chunk_size: int = 100
    chunk_overlap: int = 30
    encoding_name: str = "cl100k_base"
    
    search_k: int = 5
    lambda_mult: float = 0.15
    
    def __post_init__(self):
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
            
        self.chroma_host = os.getenv("CHROMA_HOST", self.chroma_host)
        self.chroma_port = int(os.getenv("CHROMA_PORT", str(self.chroma_port)))
        self.chroma_persist_directory = os.getenv("CHROMA_PERSIST_DIR", self.chroma_persist_directory)

vector_config = VectorConfig()