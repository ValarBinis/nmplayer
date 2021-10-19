# !/user/bin/env python3
# -*- coding:utf-8 -*-
# @Author   :  倪浩凡
# @Time     :  2021/7/10 18:58
# @File     :  nmplayer.py
# @Project  :  QT


import requests
import os
import shutil
import subprocess
from lxml import etree
from PySide2.QtCore import QFile, QStringListModel
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader


def content_xpath(html):
    content = html.content.decode('utf-8')
    return etree.HTML(content)


class Nmplayer:
    def __init__(self):
        super(Nmplayer, self).__init__()

        # 设置UI文件只读
        qfile = QFile("nmgksearch.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()

        # 加载UI文件
        self.ui = QUiLoader().load(qfile)

        # 绑定UI事件
        self.ui.potbutton.clicked.connect(self.get_pot_path)
        self.ui.searchbutton.clicked.connect(self.get_main_html)
        self.ui.resultslist.doubleClicked.connect(self.choose_movie)
        self.ui.episodelist.doubleClicked.connect(self.choose_episode)
        self.ui.playallbutton.clicked.connect(self.play_all_episode)
        self.ui.clearbutton.clicked.connect(self.clear_source)

        # 初始化参数
        self.pot_path = self.ui.potedit.text()
        self.get_pot_path()
        self.search_url = 'https://www.nmgk.com/index.php?s=vod-s-name'
        self.mother_url = 'https://www.nmgk.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'
        }
        self.search_name = ''
        self.results_name = []
        self.results_href = []
        self.pic_path = './imgs/'
        self.movie_info = ''
        self.episode_name = []
        self.episode_href = []
        self.m3u8_url = []
        self.play_all_string = ''

    def get_pot_path(self):
        self.pot_path = self.ui.potedit.text()
        if not os.path.exists('pot.config'):
            with open('pot.config', 'w') as f:
                f.write(self.pot_path)
        elif self.pot_path != '':
            with open('pot.config', 'r') as f:
                read_path = f.readline()
            if read_path != self.pot_path:
                os.remove('pot.config')
                with open('pot.config', 'w') as f:
                    f.write(self.pot_path)
        else:
            with open('pot.config', 'r') as f:
                self.pot_path = f.readline()
        self.set_placeholdertext()

    def set_placeholdertext(self):
        self.ui.potedit.setPlaceholderText(self.pot_path)

    def get_main_html(self):
        self.search_name = self.ui.searchedit.text()
        data = {
            'wd': self.search_name
        }
        main_pre_html = requests.get(url=self.search_url, params=data, headers=self.headers)
        main_html_xpath = content_xpath(main_pre_html)
        self.get_results(main_html_xpath)
        self.show_results_list()

    def get_results(self, htmlx):
        self.results_name = []
        results_name = htmlx.xpath('//div[@class="itemname"]/a/text()')
        results_update = htmlx.xpath('//div[@class="cateimg"]/a/i/text()')
        self.results_href = htmlx.xpath('//div[@class="cateimg"]/a/@href')
        for n,u in zip(results_name, results_update):
            result_str = n + '-----' + u
            self.results_name.append(result_str)

    def show_results_list(self):
        qlist = QStringListModel()
        qlist.setStringList(self.results_name)
        self.ui.resultslist.setModel(qlist)

    def choose_movie(self, index):
        movie_href = self.mother_url + self.results_href[index.row()]
        movie_pre_html = requests.get(url=movie_href, headers=self.headers)
        movie_html_xpath = content_xpath(movie_pre_html)
        self.get_movie_pic(movie_html_xpath)
        self.set_pixmap()
        self.get_movie_info(movie_html_xpath)
        self.get_episode(movie_html_xpath)
        self.set_episodelist()

    def get_movie_pic(self, htmlx):
        movie_pic_pre_url = htmlx.xpath('//div[@class="video_pic"]/a/img/@src')[0]
        pic_name = movie_pic_pre_url.split('/')[-1]
        movie_pic_url = self.mother_url + movie_pic_pre_url
        self.pic_path += pic_name
        res_pic = requests.get(url=movie_pic_url, headers=self.headers)
        # ./imgs/picname
        if not os.path.exists('./imgs'):
            os.mkdir('./imgs')
        with open(self.pic_path, 'wb') as f:
            f.write(res_pic.content)

    def set_pixmap(self):
        self.ui.piclabel.setPixmap(self.pic_path)

    def get_movie_info(self, htmlx):
        self.movie_info = htmlx.xpath("//div[@class='intro-box-txt']/p[2]/text()")[0]
        self.ui.episodeinfo.setText(self.movie_info)

    def get_episode(self, htmlx):
        self.episode_name = htmlx.xpath('//div[@id="ji_show_1_0"]/div[@class="drama_page"]/a/text()')
        self.episode_href = htmlx.xpath('//div[@id="ji_show_1_0"]/div[@class="drama_page"]/a/@href')

    def set_episodelist(self):
        qlist = QStringListModel()
        qlist.setStringList(self.episode_name)
        self.ui.episodelist.setModel(qlist)

    def choose_episode(self, index):
        episode_url = self.mother_url + self.episode_href[index.row()]
        episode_pre_html = requests.get(url=episode_url, headers=self.headers)
        episode_xpath_html = content_xpath(episode_pre_html)
        self.get_m3u8(episode_xpath_html)
        self.play_episode()

    def get_m3u8(self, htmlx):
        pre_m3u8 = htmlx.xpath('//div[@id="cms_player"]/iframe/@src')[0]
        self.m3u8_url = pre_m3u8.split('=')[-1]

    def play_episode(self):
        subprocess.Popen(self.pot_path + ' ' + self.m3u8_url + ' /autoplay')

    def play_all_episode(self):
        for href in self.episode_href:
            make_href = self.mother_url + href
            episode_pre_html = requests.get(url=make_href, headers=self.headers)
            episode_xpath_html = content_xpath(episode_pre_html)
            self.get_m3u8(episode_xpath_html)
            subprocess.Popen(self.pot_path + ' ' + self.m3u8_url + ' /add')

    def clear_source(self):
        shutil.rmtree('./imgs')


if __name__ == '__main__':
    app = QApplication()
    app.setStyle('Fusion')
    windows = Nmplayer()
    windows.ui.show()
    app.exec_()
