import requests
import configparser


class APIYandexDisk:

    def __init__(self):
        self.config = None
        self.ya_token = self.read_config()
        self.cloud_url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def create_folder(self, folder_name):
        ya_params = {
            'path': f"{folder_name}"
        }
        headers = {
            'Authorization': f'OAuth {self.ya_token}'
        }
        requests.put(self.cloud_url, params=ya_params, headers=headers)

    def upload_picture(self, folder_name, picture_name, url):
        ya_params = {

            'url': url,
            'path': f'{folder_name}/{picture_name}'
        }
        ya_headers = {
            'Authorization': f'OAuth {self.ya_token}'
        }
        requests.post(f'{self.cloud_url}upload/', params=ya_params, headers=ya_headers)

    def read_config(self):
        self.config = configparser.ConfigParser()
        self.config.read("tokens.ini")
        return self.config["YandexDisk"]["ya_token"]
