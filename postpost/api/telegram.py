import requests

from api.models import PlatformPost


def send_post_to_telegram_chat(token: str, chat_id: str, post: PlatformPost) -> dict:
    """
    Sends post to telegram chat.
    """
    tg = TgAPI(token=token)
    # TODO: Add media according to PlatformPost changes
    return tg.send_message(chat_id=chat_id, text=post.text_for_posting)


class TgAPI(object):
    """
    Local mini client for Telegram API.

    Its purpose it to share API token among the methods.
    """

    def __init__(self, token: str):
        """
        Init client.
        """
        self._url = 'https://api.telegram.org/bot{0}/'.format(token)

    def get_me(self):
        """
        Returns basic information about the bot.

        Can be used to test connection.
        """
        return requests.get(self._url + 'getMe').json()

    def send_message(
        self,
        chat_id: str,
        text: str,
        disable_notification: bool = False,
        disable_web_page_preview: bool = True,
    ) -> dict:
        """
        Sends the text message to the chat.
        """
        return self._request(
            'sendMessage',
            chat_id=chat_id,
            text=text,
            parse_mode='Markdown',
            disable_notification=disable_notification,
            disable_web_page_preview=disable_web_page_preview,
        )

    def send_photo(self, chat_id: str, photo: str, disable_notification: bool = False) -> dict:
        """
        Sends the photo to the chat.
        """
        return self._request(
            'sendPhoto',
            chat_id=chat_id,
            photo=photo,
            disable_notification=disable_notification,
        )

    def send_animation(
        self,
        chat_id: str,
        animation: str,
        disable_notification: bool,
    ) -> dict:
        """
        Sends the animation to the chat.
        """
        return self._request(
            'sendAnimation',
            chat_id=chat_id,
            animation=animation,
            disable_notification=disable_notification,
        )

    def _request(self, method_name: str, **kwargs):
        response = requests.post(self._url + method_name, json=kwargs)
        response.raise_for_status()
        return response.json()
