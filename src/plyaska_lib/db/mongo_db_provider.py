import logging
import threading

from beanie import init_beanie
from pymongo import AsyncMongoClient

from src.plyaska_lib.db.db_provider import DBProvider
from src.plyaska_lib.models.models_loader import load_beanie_models


def _load_documents():
    return load_beanie_models("src.models")


class MongoDBProvider(DBProvider):
    __is_initialized: bool = False
    __client: AsyncMongoClient | None = None

    def __init__(
        self, database: str, username: str, password: str, host: str, port: int
    ) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db = database
        self.lock = threading.Lock()
        super().__init__()

    def __get_url(self) -> str:
        return f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"

    async def connect(self):
        if not self.__client:
            with self.lock:
                if not self.__client:
                    self.__client = AsyncMongoClient(
                        self.__get_url(),
                        maxPoolSize=50,
                        minPoolSize=5,
                        connectTimeoutMS=2000,
                    )
                    logging.info("Connected to MongoDB")
        if not self.__is_initialized:
            with self.lock:
                if not self.__is_initialized:
                    loaded_documents = _load_documents()
                    logging.debug(f"Loaded documents: {loaded_documents}")
                    await init_beanie(
                        database=self.__client.plyaska_db,
                        document_models=loaded_documents,
                    )
                    self.__is_initialized = True
                    logging.info("DB is initialized with Beanie")

        return self.__client

    async def disconnect(self):
        if not self.__client:
            self.__is_initialized = False
            logging.info("DB was been disconnected")
            return
        await self.__client.close()
        self.__client = None
        self.__is_initialized = False
        logging.info("DB is disconnected")
