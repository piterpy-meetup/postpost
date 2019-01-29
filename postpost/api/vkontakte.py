from typing import List

import requests


def get_authorization_url(client_id: int, api_version: float) -> str:
    """
    Returns a string with url for authorization.

    By following the url, you will be asked by VK to give access to the application.
    After agreement, a blank page will be displayed, and there will be an access token
    in the address bar. This token is required by functions bellow.
    """
    url = (
        'https://oauth.vk.com/authorize?client_id={client_id}&response_type=token&'
        'scope=wall,offline,groups,photos,docs&v={api_version}&'
        'redirect_uri=https://oauth.vk.com/blank.html'
    ).format(
        client_id=client_id, api_version=api_version,
    )
    return url


def send_post_to_group(
    token: str, group_id: int, api_version: float, message: str, doc_path: str = None,
) -> requests.Response:
    """
    Sends post to vk group on behalf of the group itself.
    """
    vk_api = VkApi(token, api_version)
    attachments = []
    if doc_path:
        attachments.append(vk_api.upload_doc(doc_path))
    return vk_api.send_post_to_group_wall(group_id, message, attachments)


class VkApiError(Exception):
    """
    Vk API base exception.
    """
    def __init__(self, method: str, payload: dict, response: bytes):
        message = '{0} {1} {2}'.format(method, payload, response)
        super(VkApiError, self).__init__(message)


class VkApi(object):
    """
    Local mini client for vk API.
    """

    def __init__(self, token: str, api_version: float):
        """
        Init client.
        """
        self._token = token
        self._api_version = api_version
        self._url = 'https://api.vk.com/method/'

    def send_post_to_group_wall(self, group_id: int, message: str, attachments: List[str] = None):
        """
        Sends post to vk group on behalf of the group itself.
        """
        payload = {
            'owner_id': -group_id,
            'from_group': 1,
            'message': message,
        }
        if attachments:
            payload['attachment'] = ','.join(attachments)
        response = self._request('wall.post', payload=payload)
        return response

    def upload_doc(self, doc_path: str) -> str:
        """
        Uploads and saves doc on the server.
        """
        server = self._get_doc_server()
        doc_file = self._upload_doc_to_server(server, doc_path)
        doc_name = self._save_doc(doc_file)
        return doc_name

    def _get_doc_server(self) -> str:
        """
        Returns the server address for document upload.
        """
        response = self._request('docs.getWallUploadServer')
        return response['upload_url']

    def _upload_doc_to_server(self, server: str, doc_path: str) -> str:
        """
        Uploads doc to the server and returns server's file name.
        """
        response = requests.post(server, files={'file': open(doc_path, 'rb')})
        if response.status_code != requests.codes.ok or 'error' in response.json():
            raise VkApiError(server, {'file': doc_path}, response.content)
        return response.json()['file']

    def _save_doc(self, doc_file: str) -> str:
        """
        Saves the uploaded doc file on the server.
        """
        response = self._request('docs.save', {'file': doc_file})
        return 'doc{0}_{1}'.format(response['doc']['owner_id'], response['doc']['id'])

    def _request(self, method: str, payload: dict = None):
        if payload is None:
            payload = {}
        payload.update({
            'v': self._api_version,
            'access_token': self._token,
        })
        response = requests.post(self._url + method, data=payload)
        if response.status_code != requests.codes.ok or 'error' in response.json():
            raise VkApiError(method, payload, response.content)
        return response.json()['response']
