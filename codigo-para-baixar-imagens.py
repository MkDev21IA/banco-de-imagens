import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def baixar_imagens(url, pasta, quantidade):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    contador = 0
    # Scroll down to load more images
    body = driver.find_element(By.TAG_NAME, 'body')
    while contador < quantidade:
        for _ in range(5):  # Adjust the range as needed
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)  # Wait for images to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        imagens = soup.find_all('img')

        for img in imagens:
            if contador >= quantidade:
                break
            try:
                img_url = img.get('src')
                if img_url:
                    if not img_url.startswith('http'):
                        img_url = url + img_url
                    response = requests.get(img_url)
                    if 'image/jpeg' in response.headers['Content-Type']:  # Check if the image is in JPEG format
                        img_data = response.content
                        with open(os.path.join(pasta, f'sucuri_{contador}.jpg'), 'wb') as handler:
                            handler.write(img_data)
                        contador += 1
            except Exception as e:
                print(f'Erro ao baixar a imagem: {e}')

    driver.quit()

url = 'https://www.google.com/search?q=eunectes+murinus&udm=2'
pasta = 'sucuri'
quantidade = 100

baixar_imagens(url, pasta, quantidade)