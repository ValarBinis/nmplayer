# 柠檬观看 For Pot_player

### 搜索页

+ 搜索请求

  ```python
  request_url = 'https://www.nmgk.com/index.php?s=vod-s-name'
  mother_url = 'https://www.nmgk.com/'
  data{
      'wd':'瑞克和莫蒂'
  }
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'
  }
  ```

+ XPath分析

  ```python
  # reutlts_href
  //div[@class="cateimg"]/a/@href
  内容：
  /vod/8314.html
  /vod/19407.html
  /vod/10724.html
  /vod/10872.html
  /vod/10871.html
  ```

  ```python
  # results_name
  //div[@class="itemname"]/a/text()
  内容：
  瑞克和莫蒂第四季
  瑞克和莫蒂第五季
  瑞克和莫蒂第一季
  瑞克和莫蒂第三季
  瑞克和莫蒂第二季
  ```
  
  ```python
  # results_update
  //div[@class="cateimg"]/a/i/text()
  内容：
  10集全
  更新至03集
  11集全
  10集全
  10集全
  ```
  
  

### 详情页

+ 请求

  ```python
  get movie_url
  ```

+ 获取图片

  ```python
  # movie_pic
  //div[@class="video_pic"]/a/img/@src
  内容：
  /Uploads/vod/2021-03-31/6063eece12246.jpg
  ```

+ 获取描述

  ```python
  # movie_info
  //div[@class='intro-box-txt']/p[2]/text()
  内容：
  瑞克和莫蒂第五季，这是由一个个独立小故事组成，精妙无比的剧情安排，天马行空的想象力，突破天际的脑洞，是本剧最大的特点。
  ```

+ 获取集数名称

  ```python
  # episode_name_list
  //div[@id="ji_show_1_0"]/div[@class="drama_page"]/a/text()
  内容：
  第01集
  第02集
  第03集
  ```

  

+ 获取集数链接

  ```python
  # episode_href_list
  //div[@id="ji_show_1_0"]/div[@class="drama_page"]/a/@href
  内容：
  /v/19407-1-1.html
  /v/19407-1-2.html
  /v/19407-1-3.html
  ```

### 播放页

+ 获取m3u8字符串

  ```python
  # m3u8_pre_list
  //div[@id="cms_player"]/iframe/@src
  内容：
  /play.html?u=https://vod.bunediy.com/20210625/kvVyDgPY/index.m3u8
  ```

+ 逻辑

  ```python
  m3u8_string = m3u8_pre_list[0]
  m3u8 = m3u8_string.split("=")[-1]
  ```

  