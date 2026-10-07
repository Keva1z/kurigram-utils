from pyrogram import Client


class CacheChat:
    def __init__(self, chat_id: int, client: Client):
        self.chat_id: int = chat_id
        self.client: Client = client
