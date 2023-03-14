from adapters.telegram_connector import TgClient
from adapters.settings import Settings

from applications.services import KeyWordsQualifier

tg_settings = Settings()


def show_topics(main_topics):
    for datetopic in main_topics:
        print(datetopic.date)
        print(datetopic.top_keywords)


if __name__ == '__main__':
    tg_client = TgClient(
        api_id=tg_settings.API_ID,
        api_hash=tg_settings.API_HASH,
        phone=tg_settings.PHONE,
        username=tg_settings.USERNAME
    )

    # TODO будет приходить из UI:
    channel_url = 'shot_shot'
    depth_days = 15

    messages = tg_client.get_messages(
        channel_url=channel_url, depth_days=depth_days
    )

    keywords_qualifier = KeyWordsQualifier()
    main_topics = keywords_qualifier.key_words_by_days(messages.to_df())

    show_topics(main_topics)

