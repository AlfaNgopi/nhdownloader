import requests
import os
import time
import bs4

def get_links(code):
    html = requests.get('https://nhentai.net/g/' + code)
    soup = bs4.BeautifulSoup(html.content, 'html.parser')
    gallery_thumbs = soup.find_all('a', class_='gallerythumb')
    links = []
    for thumb in gallery_thumbs:
        link = thumb.find('img')['data-src']
        new_link = link.replace('t.jpg', '.jpg')
        new_link = new_link.replace('t.png', '.png')
        new_link = "https://" + "i" + new_link[9:]
        print(new_link)
        
        links.append(new_link)
    return links

def get_data(code):
    response = requests.get('http://nhentai.net/api/gallery/' + code)
    return response.json()

def get_image(link):
    while True:
        try:
            response = requests.get(link)
            break
        except:
            print('Timeout')
            time.sleep(5)
            continue
    
    return response.content

def check_extension(media_id):
    
    response = requests.get(f'https://i2.nhentai.net/galleries/{media_id}/1.jpg', timeout=1)
    print(response.status_code)
    if response.status_code == 200:
        return 'jpg'

    response = requests.get(f'https://i2.nhentai.net/galleries/{media_id}/1.png', timeout=1)
    return 'png'
        


def main():
    
    code = input('Enter the code of the doujinshi: ')
    
    data = get_data(code)
    links = get_links(code)
    data['title'] = data['title']['english']
    
    
    #export json
    with open('data.json', 'w') as f:
        import json
        json.dump(data, f, ensure_ascii=False)
        
        
    
    
    
    
    for link in links:
        image_link = link
        i = links.index(link)
        ext = link[-3:]
        image = get_image(image_link)
        
        file_path = f'out/{code}/{i+1}.{ext}'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(image)
            print(f'{code} {i+1} downloaded')
    
    
    

if __name__ == '__main__':
    main()