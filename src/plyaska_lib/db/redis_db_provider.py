import logging
import threading

from redis.asyncio import Redis

from src.plyaska_lib.db.db_provider import DBProvider


class RedisDBProvider(DBProvider):
    __client: Redis | None = None

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.lock = threading.Lock()
        super().__init__()

    async def connect(self):
        if not self.__client:
            with self.lock:
                if not self.__client:
                    self.__client = await Redis(
                        host=self.host, port=self.port, db=0
                    )
                    logging.info("Connected to Redis")

        return self.__client

    async def disconnect(self):
        if not self.__client:
            logging.info("Redis was been disconnected")
            return
        await self.__client.close()
        await self.__client.connection_pool.disconnect()
        self.__client = None
        logging.info("Redis is disconnected")
