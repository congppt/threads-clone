from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from db.database import redis_pool

class RedisPubSubManager:
    def __init__(self):
        self.pubsub = None
    
    async def __get_redis_connection_async(self) -> Redis:
        return Redis(connection_pool=redis_pool)
    
    async def connect(self):
        self.redis_connection = await self.__get_redis_connection_async()
        self.pubsub = self.redis_connection.pubsub()

    async def subscribe_async(self, channel_id: int) -> PubSub:
        await self.pubsub.subscribe(channel_id)
        return self.pubsub
    
    async def unsubscribe_async(self, channel_id: int):
        await self.pubsub.unsubscribe(channel_id)

    async def publish_async(self, channel_id: int, message: str):
        await self.redis_connection.publish(channel_id, message)

    async def disconnect_async(self):
        await self.redis_connection.aclose()