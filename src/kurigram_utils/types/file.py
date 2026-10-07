import logging
from os import PathLike

from pyrogram import Client
from pyrogram.types import InputMediaPhoto, InputMediaVideo, Message

from kurigram_utils.cache import get_cache

log = logging.getLogger(__name__)


class File:
    def __init__(self, path: str | PathLike[str]):
        self.path: str | PathLike[str] = path
        self._cache: str | None = None

    def __check_connection(self) -> bool:
        cache = get_cache()
        return bool(cache and cache.client.is_connected)

    @property
    def single(self) -> str | PathLike[str]:
        return self._cache or self.path

    @property
    def group(self) -> InputMediaPhoto | InputMediaVideo:
        raise NotImplementedError("Subclasses must implement the 'group' property.")

    async def _send(
        self,
        chat_id: int,
        client: Client,
    ) -> Message | None:
        """Should return a Message if the file is sent successfully, otherwise None. Cache should be set in this method."""
        raise NotImplementedError

    async def _create_cache(self) -> None:
        cache = get_cache()
        if not cache or not self.__check_connection():
            return

        message = await self._send(cache.chat_id, cache.client)

        if message:
            await message.delete()

            log.info(
                f"Cached file {self.path} in chat {cache.chat_id} with file_id {self._cache}."
            )


class Files:
    @classmethod
    async def prepare(cls):
        for value in vars(cls).values():
            if isinstance(value, File):
                await value._create_cache()


class Photo(File):
    def __init__(self, path: str | PathLike[str]):
        super().__init__(path)

    @property
    def group(self) -> InputMediaPhoto:
        return InputMediaPhoto(self.single)

    async def _send(self, chat_id: int, client: Client) -> Message | None:
        message: Message | None = await client.send_photo(chat_id, self.path)

        if message and message.photo:
            self._cache = message.photo.file_id
            return message

        return None


class Video(File):
    def __init__(self, path: str | PathLike[str]):
        super().__init__(path)

    @property
    def group(self) -> InputMediaVideo:
        return InputMediaVideo(self.single)

    async def _send(self, chat_id: int, client: Client) -> Message | None:
        message: Message | None = await client.send_video(chat_id, self.path)

        if message and message.video:
            self._cache = message.video.file_id
            return message

        return None
