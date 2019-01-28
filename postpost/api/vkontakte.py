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
    payload = {
        'owner_id': -group_id,
        'from_group': 1,
        'message': message,
        'access_token': token,
        'v': api_version,
    }
    attachments = []
    if doc_path:
        attachments.append(upload_doc(token, api_version, doc_path))
    if attachments:
        payload['attachment'] = ','.join(attachments)
    response = requests.post('https://api.vk.com/method/wall.post', data=payload)
    return response


def upload_doc(token: str, api_version: float, file_path: str) -> str:
    """
    Uploads and saves doc on the server.
    """
    server = get_doc_upload_server(token, api_version)
    doc_file = upload_doc_to_server(server, file_path)
    doc_name = save_doc(token, api_version, doc_file)
    return doc_name


def get_doc_upload_server(token: str, api_version: float) -> str:
    """
    Returns the server address for document upload.
    """
    response = requests.get(
        'https://api.vk.com/method/docs.getWallUploadServer', params={
            'access_token': token,
            'v': api_version,
        },
    )
    return response.json()['response']['upload_url']


def upload_doc_to_server(server: str, file_path: str) -> str:
    """
    Uploads doc to the server and returns server's file name.
    """
    response = requests.post(server, files={'file': open(file_path, 'rb')})
    return response.json()['file']


def save_doc(token: str, api_version: float, doc_file: str) -> str:
    """
    Saves the uploaded doc file on the server.
    """
    response = requests.post(
        'https://api.vk.com/method/docs.save', data={
            'access_token': token,
            'file': doc_file,
            'v': api_version,
        },
    )
    doc = response.json()['response']['doc']
    return 'doc{0}_{1}'.format(doc['owner_id'], doc['id'])
