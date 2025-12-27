from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Dict, Any, List
import logging
from ..config import settings
from .models import ReviewSession

logger = logging.getLogger(__name__)

class MongoDBClient:
    """Async MongoDB client wrapper."""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[settings.MONGO_DB_NAME]
            # Verify connection
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    async def save_review(self, review: ReviewSession) -> str:
        """Save or update a review session."""
        if not self.db:
            await self.connect()
            
        result = await self.db.reviews.update_one(
            {"id": review.id},
            {"$set": review.model_dump()},
            upsert=True
        )
        return review.id

    async def get_review(self, review_id: str) -> Optional[ReviewSession]:
        """Retrieve a review session."""
        if not self.db:
            await self.connect()
            
        data = await self.db.reviews.find_one({"id": review_id})
        if data:
            return ReviewSession(**data)
        return None

# Global instance
mongo_client = MongoDBClient()
