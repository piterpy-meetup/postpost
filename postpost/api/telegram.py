import requests

from api.models import PlatformPost
from custom_types import JSON


def send_post_to_telegram_chat(token: str, chat_id: str, post: PlatformPost) -> JSON:
    """
    Sends post to telegram chat.
    """
    tg = TgAPI(token=token, chat_id=chat_id)
    # TODO: Add media according to PlatformPost changes
    return tg.send_message(text=post.text_for_posting)


class TgAPI(object):
    """
    Local mini client for Telegram API.

    Its purpose it to share API token and chat id among the methods.
    """

    def __init__(self, token: str, chat_id: str):
        """
        Init client.
        """
        self._url = 'https://api.telegram.org/bot{0}/'.format(token)
        self._chat_id = chat_id

    def send_message(
        self,
        text: str,
        disable_notification: bool = False,
        disable_web_page_preview: bool = True,
    ) -> JSON:
        """
        Sends the text message to the chat.
        """
        return self._request(
            'sendMessage',
            chat_id=self._chat_id,
            text=text,
            parse_mode='Markdown',
            disable_notification=disable_notification,
            disable_web_page_preview=disable_web_page_preview,
        )

    def send_photo(self, photo: str, disable_notification: bool = False) -> JSON:
        """
        Sends the photo to the chat.
        """
        return self._request(
            'sendPhoto',
            chat_id=self._chat_id,
            photo=photo,
            disable_notification=disable_notification,
        )

    def send_animation(self, animation: str, disable_notification: bool = False) -> JSON:
        """
        Sends the animation to the chat.
        """
        return self._request(
            'sendAnimation',
            chat_id=self._chat_id,
            animation=animation,
            disable_notification=disable_notification,
        )

    def _request(self, method_name: str, **kwargs) -> JSON:
        response = requests.post(self._url + method_name, json=kwargs)
        response.raise_for_status()
        json: JSON = response.json()
        return json
