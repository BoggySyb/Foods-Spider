from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import re


# 指定 WebDriver 的路径，需要将其替换为你自己系统的 WebDriver 路径
driver_path = "/usr/local/bin/chromedriver"

def get_food_info(food_url):
    driver = webdriver.Chrome(driver_path)
    driver.get(food_url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 做法
    process = soup.find('div', class_='info2_item info2_item1').find('strong').get_text()
    # 味道
    taste = soup.find('div', class_='info2_item info2_item2').find('strong').get_text()
    # 时间
    time = soup.find('div', class_='info2_item info2_item3').find('strong').get_text()
    # 难度
    difficulty = soup.find('div', class_='info2_item info2_item4').find('strong').get_text()

    s = soup.find('span', class_='info1').get_text()
    numbers = re.findall(r'\d+', s)

    # 收藏,浏览
    collections, looks = int(numbers[0]), int(numbers[1])

    driver.quit()
    return [process, taste, time, difficulty, collections, looks]


def food_scrawler(url, num_page=1):
    food_data = [["Name", "Author", "Process", "Taste", "Time", "Difficulty", "Collections", "Looks"]]

    for i in range(1, num_page+1):
        driver = webdriver.Chrome(driver_path)
        driver.get(url + f'p{i}/')

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        food_items = soup.find_all('div', class_='list_s2_item')

        for food in food_items:
            food_info = []
            # name 名字
            food_info.append(food.find('strong', class_='title').get_text())
            # author 作者
            food_info.append(food.find('a', class_='list_s2_item_author').find('strong').get_text())
            # Img url
            # food_data.append(food.find('a', class_='list_s2_item_author'))
            # 美食 url
            food_url = food.find('a', class_='list_s2_item_img')['href']
            food_info.extend(get_food_info(food_url))
            food_data.append(food_info)

        driver.quit()

    with open('foods.csv', 'w') as file:
        csv_writer = csv.writer(file)
        # 写入数据
        csv_writer.writerows(food_data)

url = "https://www.meishij.net/"
classes_url = "https://www.meishij.net/caipufenlei/"
class_url = "https://www.meishij.net/fenlei/zaocan/"
class_url_p2 = "https://www.meishij.net/fenlei/wucan/p2/"
food_url = "https://www.meishij.net/zuofa/jidantudousibing.html"

food_scrawler(class_url, 2)