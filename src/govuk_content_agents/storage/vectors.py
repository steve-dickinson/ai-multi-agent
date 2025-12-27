import psycopg2
from pgvector.psycopg2 import register_vector
from typing import List, Dict, Any, Optional
import logging
from ..config import settings
from .models import ContentEmbedding

logger = logging.getLogger(__name__)

class VectorDBClient:
    """PostgreSQL + pgvector client wrapper."""
    
    def __init__(self):
        self.conn = None
        
    def connect(self):
        """Connect to PostgreSQL."""
        try:
            self.conn = psycopg2.connect(settings.POSTGRES_URI)
            # Register pgvector extension
            cur = self.conn.cursor()
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            register_vector(self.conn)
            self.conn.commit()
            
            # Create table if not exists (simple synchronous setup)
            self._init_table()
            
            logger.info("Successfully connected to PostgreSQL/pgvector")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    def _init_table(self):
        """Initialize the vectors table."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS content_embeddings (
            id UUID PRIMARY KEY,
            content TEXT,
            embedding vector(1536),
            metadata JSONB,
            created_at TIMESTAMP
        );
        """
        if not self.conn:
            return
            
        with self.conn.cursor() as cur:
            cur.execute(create_table_sql)
            self.conn.commit()

    def close(self):
        """Close connection."""
        if self.conn:
            self.conn.close()

    def save_embedding(self, item: ContentEmbedding):
        """Save an embedding."""
        if not self.conn:
            self.connect()
            
        sql = """
        INSERT INTO content_embeddings (id, content, embedding, metadata, created_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            content = EXCLUDED.content,
            embedding = EXCLUDED.embedding,
            metadata = EXCLUDED.metadata,
            created_at = EXCLUDED.created_at;
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, (
                item.id,
                item.content,
                item.embedding,
                json.dumps(item.metadata) if item.metadata else '{}',
                item.created_at
            ))
            self.conn.commit()

    def search_similar(self, embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar content."""
        if not self.conn:
            self.connect()
            
        sql = """
        SELECT id, content, metadata, 1 - (embedding <=> %s::vector) as similarity
        FROM content_embeddings
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """
        results = []
        with self.conn.cursor() as cur:
            cur.execute(sql, (embedding, embedding, limit))
            rows = cur.fetchall()
            for row in rows:
                results.append({
                    "id": row[0],
                    "content": row[1],
                    "metadata": row[2],
                    "similarity": row[3]
                })
        return results

import json
from openai import OpenAI
from ..config import settings
from .models import generate_uuid, ContentEmbedding
from datetime import datetime

# Global instance
vector_client = VectorDBClient()

class VectorService:
    """High-level service for vector operations (embedding + storage)."""
    
    def __init__(self):
        self.client = vector_client
        self.openai = OpenAI(api_key=settings.OPENAI_API_KEY)

    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for text using OpenAI."""
        response = self.openai.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def upsert_policy(self, content: str, metadata: dict[str, Any]) -> str:
        """Generate embedding and save to DB."""
        embedding = self.embed_text(content)
        doc_id = generate_uuid()
        
        item = ContentEmbedding(
            id=doc_id,
            content=content,
            embedding=embedding,
            metadata=metadata,
            created_at=datetime.utcnow()
        )
        
        self.client.save_embedding(item)
        return doc_id

# Service instance
vector_service = VectorService()
