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

# Global instance
vector_client = VectorDBClient()
