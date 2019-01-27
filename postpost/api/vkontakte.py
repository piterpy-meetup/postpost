from typing import List

import requests


def get_authorization_url(client_id: int, api_version: float) -> str:
    """
    Returns a string with url for authorization.
    """
    url = """
    https://oauth.vk.com/authorize?client_id={client_id}&scope=wall,offline,groups
    redirect_uri=https://oauth.vk.com/blank.html&response_type=token&v={api_version}""".format(
        client_id=client_id, api_version=api_version,
    )
    return url


def send_post_to_group(
    token: str, group_id: int, api_version: float, message: str, attachments: List[str],
) -> requests.Response:
    """
    Sends post to vk group on behalf of the group itself.
    """
    response = requests.post('https://api.vk.com/method/wall.post', data={
        'owner_id': group_id,
        'from_group': 1,
        'message': message,
        'access_token': token,
        'v': api_version,
        'attachment': ','.join(attachments),
    })
    return response
