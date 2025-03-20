import requests


response = requests.get("https://i2.nhentai.net/galleries/2052895/1.png")
with open("1.jpg", "wb") as f:
    f.write(response.content)
    print(1)
