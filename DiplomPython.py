#!/usr/bin/env python
# coding: utf-8

# In[33]:


from pprint import pprint
import os
import json
import requests

def vk_token(file):
    with open(file , 'r', encoding='utf-8') as file:
        vk_token = file.read().strip()
        return vk_token


class Basic():
    def __init__(self, token: str, user_id: str):
        self.token = token
        self.headers_Ya = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        self.user_id = user_id

    def photosVK(self): 
        params = {'access_token':vk_token('token_vk.txt') ,
                       'owner_id': self.user_id,
                       'photo_sizes': '1',
                       'album_id': 'profile',
                       'extended': '1',
                       'count': '5', 
                       'v': 5.131}
        get_photos= requests.get('https://api.vk.com/method/photos.get', params=params).json()['response']['items']
        file_photo = []  
        for photo in get_photos:
            file_photo.append({'likes': photo['likes']['count'], 'date_upload': photo['date'],
                               'link': photo['sizes'][-1], 'size': photo['sizes'][-1]['type']})
        sort_photo = sorted(file_photo, key=lambda x: x['likes'])
        photo_list = {}  
        photo_list_1 = [] 
        for photo in sort_photo:
            likes = photo['likes']
            size = photo['size']
            if f'{likes}.jpg' not in list(photo_list.keys()):
                file_name = f'{likes}.jpg'
                photo_list[file_name] = photo['link']
            else:
                rename = str(likes) + str(photo['date_upload'])
                file_name = f'{rename}.jpg'
                photo_list[file_name] = photo['link']
            photo_list_1.append({'file_name': file_name, 'size': size})
        with open ('photo.json', 'w', encoding='utf-8') as file:  
            k = file.write(json.dumps(photo_list_1))
        for photo, link in photo_list.items():            
            image = requests.get(link['url'])
            full_file_name = os.path.join('Photo', photo)
            with open(full_file_name, 'wb') as file:
                file.write(image.content)
        print('Изображения сохранены в папку Photo')
        return print()
    
    
    def upload_photos(self, path):    
        self.path = path
        file_list = os.listdir(self.path)    
        path_list = []                        
        for file in file_list:
            path = os.path.join(self.path, file)
            path_list.append(path)
        create_folder = requests.put('https://cloud-api.yandex.net/v1/disk/resources?path=%2FPhoto',   
                                     headers=self.headers_Ya)
        for i, path1 in enumerate(path_list, 1):  
            with open(path1, 'rb') as f:
                _file = f.read()
                                                     
            response = requests.get(f'https://cloud-api.yandex.net/v1/disk/resources/upload?path=%2FPhoto/{os.path.basename(path1)}',
                                       headers=self.headers_Ya).json()
            print(response)
            link_upload = response['href']
            operation_id = response['operation_id']
            upload = requests.put(link_upload, headers=self.headers_Ya, data=_file)  
            while True:  
                status = requests.get(f'https://cloud-api.yandex.net/v1/disk/operations/{operation_id}', headers=self.headers_Ya).json()['status']
                if status == 'success':
                    break
            print(f'Изображение "{os.path.basename(path1)}" {str(i)}/{str(len(path_list))} загружено на диск')
        print()
        return print('Завершено')


# In[ ]:





# In[ ]:


if __name__ == '__main__':
    token_ya= input('Введите токен с Полигона Яндекс.Диска ')
    user_id = input('Введите id пользователя VK ')
    my_file_path = r'Photo'
    user = Basic(token_ya, user_id)  
    user.photosVK()
    user.upload_photos(my_file_path)


# In[ ]:





# In[ ]:




