import requests
import json
import time
token = ''

class API_get_ip:
    def __init__(self):
        self.url_get_ip = 'https://api.ipify.org/?format=json'
        self.response=requests.get(self.url_get_ip)
        self.ip_number = self.response.json()['ip']
        
    def get_info_ip(self):
        self.url_ip_info = 'https://ipinfo.io/'
        self.response=requests.get(self.url_ip_info,self.ip_number)
        self.info_ip = self.response.json()
    
        with open('info_ip.txt','w',encoding='utf-8') as file:
            file.write(json.dumps(self.info_ip))

class API_yandex_disk:
    def __init__(self,token):
        self.url_yandex_disk = 'https://cloud-api.yandex.net/'
        self.headers = {'Authorization': f'OAuth {token}'}
        
        
    def create_folder(self,path):      
        response=requests.put(f'{self.url_yandex_disk}v1/disk/resources',
                              headers=self.headers,
                              params={'path':path})
        if response.status_code == 201:
            print('Папка создана')
        return  response.status_code == 201

    def upload_file(self,path_file,path_yd):
        self.response=requests.get(f'{self.url_yandex_disk}v1/disk/resources/upload',headers=self.headers,params={'path':path_yd,'overwrite':True})
        url_put_file = self.response.json()['href']
        self.response=requests.put(url_put_file,headers=self.headers,files={'file':open(path_file,'rb')})
        return self.response.status_code == 200


if __name__ == '__main__':
    API_get_ip = API_get_ip() # получаем ip
    API_get_ip.get_info_ip() # получаем информацию о ip
    API_yandex_disk = API_yandex_disk(token) # авторизуемся на яндекс диске
    API_yandex_disk.create_folder('ip_info') # создаем папку 
    API_yandex_disk.upload_file('info_ip.txt','ip_info/info_ip.txt') # загружаем файл