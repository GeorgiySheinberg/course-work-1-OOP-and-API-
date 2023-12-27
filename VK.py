import requests
import configparser


class VKAPI:

    def __init__(self):
        self.config = None
        self.vk_token = self.read_config()
        self.api_base_url = 'https://api.vk.com/method/'
        self.user_id = self.get_users_id()

    def get_vk_photo_params(self):  # Возвращает параметры для загрузки фото
        params_vk = {
            'access_token': self.vk_token,
            'v': '5.199&p1=v1',
            'owner_id': self.user_id,
            'extended': 1,
            'photo_sizes': 1,
        }
        return params_vk

    def get_users_id(self):  # Пользователь вводит id или screen_name, возвращает id.
        user_input = input("Введите id пользователя или screen_name:\n")
        params_vk = {
                'access_token': self.vk_token,
                'v': '5.199&p1=v1',
                'user_ids': user_input
            }
        vk_response = requests.get(f'{self.api_base_url}users.get', params=params_vk)
        return vk_response.json().get('response')[0].get('id')

    def get_all_albums(self):  # Возвращает словарь с альбомами пользователей в формате (id: Название).
        params_vk = self.get_vk_photo_params()
        vk_album_dict = {}
        for album in ['profile', 'saved', 'wall']:
            vk_params = self.get_vk_photo_params()
            vk_params.update({'album_id': album})
            vk_photos_response = requests.get(f'{self.api_base_url}photos.get', params=vk_params)
            if vk_photos_response.json().get('response').get('count') == 0:
                continue
            else:
                vk_album_dict.update({vk_photos_response.json().get('response').get('items')[0].get('album_id'): album})
        vk_photos_response = requests.get(f'{self.api_base_url}photos.getAlbums', params=params_vk)
        for album in vk_photos_response.json().get('response').get('items'):
            vk_album_dict.update({album.get('id'): album.get('title')})
        return vk_album_dict

    def get_photos_info(self):  # Возвращает словарь со всеми фото из всех альбомов (всех размеров).
        params_vk = self.get_vk_photo_params()
        photos_info = {}
        for album_id, album_name in self.get_all_albums().items():
            params_vk.update({'album_id': album_id})
            vk_photos_response = requests.get(f'{self.api_base_url}/photos.get', params=params_vk)
            photos_info.setdefault(album_name, vk_photos_response.json().get('response'))
        return photos_info

    def read_config(self):
        self.config = configparser.ConfigParser()
        self.config.read("tokens.ini")
        return self.config["VK"]["vk_token"]
