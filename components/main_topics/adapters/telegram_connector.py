from datetime import datetime, timedelta, timezone

from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient

from .dto import MessagesTable


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

    def get_messages(
            self, channel_url: str, depth_days: int, limit: int = 10000
    ) -> MessagesTable:
        # TODO если канал закрытый, то вернуть сообщение

        channel_entity = self.client.get_entity(channel_url)

        messages_table = MessagesTable(data=dict())
        idx = 0
        max_depth_date = datetime.now(timezone.utc) - timedelta(days=depth_days)

        message_queue = self.client.iter_messages(channel_entity, limit=limit)

        for message in message_queue:
            # if we get all message of needed depth - break
            if message.date < max_depth_date:
                break

            idx += 1
            messages_table.data[idx] = {
                'datetime': message.date,
                'text': message.message
            }

        print(len(messages_table))

        return messages_table
