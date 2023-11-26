import requests
from tqdm.notebook import tqdm_notebook
import json
from tqdm import trange, tqdm


class VKtoYaDisk:
    api_base_url = 'https://api.vk.com/method/'
    cloud_url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self, vk_token, user_id, ya_token):
        self.token = vk_token
        self.user_id = user_id
        self.ya_token = ya_token

    def create_folder(self, folder_name):
        if folder_name is None:
            folder_name = 'Profile Photos'
        ya_params = {
            'path': f"{folder_name}"
        }
        headers = {
            'Authorization': f'OAuth {self.ya_token}'
        }
        ya_response = requests.put(self.cloud_url, headers=headers, params=ya_params)
        print(ya_response)

    def upload_picture(self, folder_name, picture_name):
        ya_params = {
            'path': f'{folder_name}/{picture_name}'
        }
        ya_headers = {
            'Authorization': f'OAuth {self.ya_token}'
        }
        ya_response = requests.get(f'{self.cloud_url}upload/', params=ya_params, headers=ya_headers)
        url_for_upload = ya_response.json().get('href')

        with open(picture_name, 'rb') as file:
            ya_response = requests.put(url_for_upload, files={"file": file})

    def get_vk_photo_params(self):
        params_vk = {
            'access_token': self.token,
            'v': '5.199&p1=v1',
            'owner_id': self.user_id,
            'extended': 1,
            'photo_sizes': 1,
        }
        return params_vk

    def get_all_albums(self):
        params_vk = {
            'access_token': self.token,
            'v': '5.199&p1=v1',
            'owner_id': self.user_id
        }
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

    def get_all_photos(self):
        params_vk = self.get_vk_photo_params()
        names = set()
        photos_info = {'items': []}
        for album in self.get_all_albums().keys():
            params_vk.update({'album_id': album})
            vk_photos_response = requests.get(f'{self.api_base_url}/photos.get', params=params_vk)
            self.create_folder(self.get_all_albums().get(album))
            photo = vk_photos_response.json().get('response').get('items')
            for i in tqdm(range(vk_photos_response.json().get('response').get('count')),
                          desc=f'Uploading album: {self.get_all_albums().get(album)}'):
                if photo[i].get('likes').get('count') in names:
                    with (open(f"{str(photo[i].get('likes').get('count')) + '.' + str(photo[i].get('date'))}.jpg", 'wb')
                          as f):
                        picture_name = f"{str(photo[i].get('likes').get('count')) + '.' + str(photo[i].get('date'))}.jpg"
                        response_vk = requests.get(photo[i].get('sizes')[-1].get('url'))
                        f.write(response_vk.content)
                else:
                    with open(f"{photo[i].get('likes').get('count')}.jpg", 'wb') as f:
                        response_vk = requests.get(photo[i].get('sizes')[-1].get('url'))
                        f.write(response_vk.content)
                        names.add(photo[i].get('likes').get('count'))
                        picture_name = f"{photo[i].get('likes').get('count')}.jpg"
                self.upload_picture(self.get_all_albums().get(album), picture_name)
                photos_info.get('items').append(vk_photos_response.json().get('response').get('items'))
        with open('Photos Info.json', 'w') as f:
            json.dump(photos_info, f, ensure_ascii=False, indent=2)
        return


if __name__ == '__main__':
    vk_client = VKtoYaDisk(vk_token='', user_id='', ya_token='')
    vk_client.get_all_photos()
