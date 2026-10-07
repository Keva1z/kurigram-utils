from os import PathLike

from pyrogram.types.messages_and_media.message import Message

from .cache import CacheChat


class File:
    def __init__(self, path: str | PathLike[str], cache: CacheChat | None = None):
        self.path: str | PathLike[str] = path
        self._cache: str | None = None
        self._cacheChat: CacheChat | None = cache

    def __check_connection(self) -> bool:
        return bool(self._cacheChat and self._cacheChat.client.is_connected)

    @property
    async def data(self) -> str | PathLike[str]:
        if self._cache:
            return self._cache

        if not self.__check_connection():
            return self.path

        await self._create_cache()

        return self._cache or self.path

    async def _create_cache(self) -> None:
        raise NotImplementedError


class Photo(File):
    def __init__(self, path: str | PathLike[str], cache: CacheChat | None = None):
        super().__init__(path, cache)

    async def _create_cache(self) -> None:

        if not self._cacheChat:
            return

        client = self._cacheChat.client
        chat_id = self._cacheChat.chat_id

        message: Message | None = await client.send_photo(chat_id, self.path)

        if message and message.photo:
            self._cache = message.photo.file_id
