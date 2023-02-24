from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import PeerChannel


class TgClient:
    def __init__(self, api_id: int, api_hash: str, phone: str, username: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.username = username
        self.client: TelegramClient = self._start_client()

    def _start_client(self):
        # Create the client and connect
        client = TelegramClient(self.username, self.api_id, self.api_hash)
        client.start(phone=self.phone)
        print("Client Created")

        # Ensure you're authorized
        if not client.is_user_authorized():
            client.send_code_request(self.phone)
            try:
                client.sign_in(self.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                client.sign_in(password=input('Password: '))

        return client

    def get_messages(self, channel_url: str):
        channel_entity = self.client.get_entity(channel_url)

        # get list of messages
        offset_id = 0
        limit = 100
        all_messages = []
        total_messages = 0
        total_count_limit = 0

        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
            history = self.client.get_messages(channel_url, limit=100)

            for message in history:
                all_messages.append(message.message.to_dict())

            total_messages = len(all_messages)
