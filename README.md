## 爬虫作业—对[美食杰](https://www.meishij.net)网站的美食数据爬取

![image-20231030201241146](https://p.ipic.vip/2sna59.png)

#### 项目介绍：

因为后面希望做个美食推荐系统，故正好利用这次课程机会爬取美食数据。综合考虑几个不同的美食信息网站，最后选择爬取美食杰，因为其美食属性更丰富，且有浏览、收藏等适用于推荐算法练习的信息。

------

首先尝试了最基础的爬虫框架对网站信息进行爬取，但发现返回信息为空。检查发现因为网站内容是通过 JavaScript 动态加载，Python 的 requests 库将无法正常工作，因为它无法运行 JavaScript。

```python
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def get_food_info(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    food_items = soup.find_all('div', class_='listtyle1')

    food_info = []

    for food in food_items:
        food_title = food.find('a').get('title')
        food_info.append({
            'title': food_title,
        })

    return food_info

url = "https://www.meishij.net/"
print(get_food_info(url))
```

调查之后选择了使用  Selenium 浏览器自动化工具，它能够模拟真实浏览器的行为，包括 JavaScript 的解析并渲染页面，来获取动态加载的内容。以谷歌浏览器为例，下载对应版本的 ChromeDriver，保存地址为 driver_path。

```python
from bs4 import BeautifulSoup
from selenium import webdriver

# 指定 WebDriver 的路径，需要将其替换为你自己系统的 WebDriver 路径
driver_path = "/path/to/chromedriver"

def get_food_info(url):
    driver = webdriver.Chrome(driver_path)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    food_items = soup.find_all('div', class_='listtyle1')

    food_info = []

    for food in food_items:
        food_title = food.find('a').get('title')
        food_info.append({
            'title': food_title,
        })

    driver.quit()

    return food_info

url = "https://www.meishij.net/"
print(get_food_info(url))
```

注：谷歌浏览器会自动更新，新版本没有 ChromeDriver，故需要取消自动更新

```cmd
defaults write com.google.Keystone.Agent checkInterval 0 # mac
```

对不同类别的美食进行爬取，得到下面html信息（网址: https://www.meishij.net/caipufenlei/"具体类别"）

```html
<div class="list_s2_item">
  <div class="imgw">
  <a class="list_s2_item_img" href="https://www.meishij.net/zuofa/jianmibing_3.html" style="background:url(https://s1.st.meishij.net/r/41/203/113291/s113291_154340022529574.jpg) center no-repeat;background-size:cover;"></a>
  <a class="list_s2_item_author" href="https://i.meishij.net/cook.php?id=113291">
    <div class="author_avatar" style="background:url(https://s1.st.meishij.net/user/41/203/st113291_86576.jpg) center no-repeat;background-size:cover;"></div>
    <strong>美食小编</strong>
   </a>
  </div>
  <a class="list_s2_item_info" href="">
    <strong class="title">煎米饼</strong>
    <span class="sc">火腿肠,鸡蛋,熟米饭</span>
  </a>
</div>
```

从中可以得到美食名字，图片url，作者，美食网页url。嵌套循环访问美食网页url，得到工艺、口味、时间、难度等更详细的信息。（网址: https://www.meishij.net/caipufenlei/"具体类别"/"美食名称"）

![image-20231030205057572](https://p.ipic.vip/hnz9fr.png)

```html
<div class="info2">
  <div class="info2_item info2_item1"><em>工艺</em> <strong>煎</strong></div>
  <div class="info2_item info2_item2"><em>口味</em> <strong>黑椒味</strong></div> 
  <div class="info2_item info2_item3"><em>时间</em> <strong>10分钟</strong></div> 
  <div class="info2_item info2_item4"><em>难度</em> <strong>初级入门</strong></div>
</div>
```

最后将爬取到的数据保存到 csv 文件中

```python
  with open('foods.csv', 'w') as file:
      csv_writer = csv.writer(file)
      food_data = [["Name", "Author", "Image_url", "Process", "Taste", "Time", "Difficulty", "Collections", "Looks"]]
			food_data.extend(food_list)
      # 写入数据
      csv_writer.writerows(food_data)
```

csv 样例数据如下，到此，爬虫完成

```csv
Name,Author,Process,Taste,Time,Difficulty,Collections,Looks
土豆饼,美食小编,煎,家常味,15分钟,初级入门,727,3796
土豆丝卷饼,美食小编,煎,香辣味,15分钟,初级入门,12899,2096
煎米饼,美食小编,煎,咸鲜味,30分钟,初中水平,4109,1503
酱油炒饭,美食小编,炒,家常味,15分钟,初级入门,620,2230
梅森杯素食沙拉,龙宝宝陈诺（陈筱盈）,煮,家常味,5分钟,新手尝试,3242,6522
营养早餐烤鸡蛋,萌城美食,烤,家常味,30分钟,初级入门,368,12077
银耳红枣汤,美食小编,煮,咸鲜味,10分钟,初级入门,589,3326
蛋挞,美食小编,烘焙,甜味,30分钟,初级入门,14630,3405
宫廷牛肉酥饼,一枝独秀1987,烙,咸鲜味,10分钟,未知,1987,459
燕麦片粥,美食小编,煲,奶香味,30分钟,新手尝试,1576,2031
蒸鸡蛋羹,征服之海,蒸,咸鲜味,10分钟,初级入门,1293,221625
```

