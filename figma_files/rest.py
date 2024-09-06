import requests


def get_file(file_key, api_token):
    headers = {"X-Figma-Token": api_token}
    url = f"https://api.figma.com/v1/files/{file_key}"
    response = requests.get(url, headers=headers)
    return response


def get_images(file_key, api_token):
    headers = {"X-Figma-Token": api_token}
    url = f"https://api.figma.com/v1/files/{file_key}/images"
    response = requests.get(url, headers=headers)
    return response
