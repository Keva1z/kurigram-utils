from pyrogram import Client

from .types.cache import CacheChat

_CACHE: None | CacheChat = None


def setup_file_cache(client: Client, chat_id: int) -> None:
    """
    Sets up a cache chat for the given client and chat ID.

    Args:
        client (Client): The Pyrogram client instance.
        chat_id (int): The ID of the chat to be used for caching.

    Returns:
        CacheChat: An instance of CacheChat containing the chat ID and client.
    """

    global _CACHE
    _CACHE = CacheChat(chat_id=chat_id, client=client)
