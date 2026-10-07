from pyrogram import Client


class CacheChat:
    def __init__(self, chat_id: int, client: Client):
        self.chat_id: int = chat_id
        self.client: Client = client


_CACHE: None | CacheChat = None


def get_cache() -> None | CacheChat:
    """
    Returns the current cache chat if it exists, otherwise returns None.

    Returns:
        None | CacheChat: The current cache chat or None if not set.
    """
    return _CACHE


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
