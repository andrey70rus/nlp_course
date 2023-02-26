from adapters.telegram_connector import TgClient
from adapters.settings import Settings

tg_settings = Settings()

if __name__ == '__main__':
    tg_client = TgClient(
        api_id=tg_settings.API_ID,
        api_hash=tg_settings.API_HASH,
        phone=tg_settings.PHONE,
        username=tg_settings.USERNAME
    )

    # TODO будет приходить из UI:
    channel_url = 'ru2ch_news'
    depth_days = 10

    messages = tg_client.get_messages(
        channel_url=channel_url, depth_days=depth_days
    )

    print(messages.to_df())
