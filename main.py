import json
from tqdm import trange, tqdm
from VK import VKAPI
from Yandex import APIYandexDisk
import datetime


def date_in_name(date):  # Из unix time в datetime
    return datetime.datetime.fromtimestamp(date).strftime("%d.%m.%Y")


def album_selection():  # Создаем список из альбомов, выбираем нужные
    user_albums = user.get_all_albums()
    album_names_list = []
    for album in user_albums.values():
        album_names_list.append(album)
    user_input = input(f"Введите через запятую названия альбомов из списка: {', '.join(album_names_list)}\n")
    album_list = user_input.split(', ')
    return album_list


def upload_chosen_photos():
    vk_photo_unique_names = set()
    photos = {'uploaded photos': []}
    for album_name in album_selection():
        photos_amount = input(f"Введите количество фотографий из альбома '{album_name}':\n")
        user2 = APIYandexDisk()
        all_photos = user.get_photos_info()
        try:
            if int(photos_amount) > all_photos.get(album_name).get('count'):
                photos_amount = all_photos.get(album_name).get('count')
        except ValueError:
            photos_amount = 5
            if photos_amount > all_photos.get(album_name).get('count'):
                photos_amount = all_photos.get(album_name).get('count')
        user2.create_folder(album_name)
        for i in tqdm(trange(int(photos_amount), desc='Uploading Photo')):
            vk_photo_url = all_photos.get(album_name).get('items')[i].get('sizes')[-1].get('url')
            vk_photo_name = all_photos.get(album_name).get('items')[i].get('likes').get('count')
            if vk_photo_name in vk_photo_unique_names:
                path = all_photos.get(album_name).get("items")[i].get("date")
                vk_photo_name = f'{vk_photo_name} {date_in_name(path)}'
            else:
                vk_photo_unique_names.add(vk_photo_name)
            user2.upload_picture(album_name, vk_photo_name, vk_photo_url)
            size_path = all_photos.get(album_name).get('items')[i].get('sizes')[-1].get('type')
            photos.get('uploaded photos').append({'Album': album_name, 'file_name': vk_photo_name, "size": size_path})
    with open('Загруженные фотографии.json', 'w') as f:
        json.dump(photos, f, ensure_ascii=False, indent=2)
    return


if __name__ == '__main__':
    user = VKAPI()
    upload_chosen_photos()
