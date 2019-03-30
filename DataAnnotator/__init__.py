# -*- coding: utf-8 -*-
# __init__.py
# GUIの立ち上げにまつわることを書く　main.kv読み込み

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from DataAnnotator import FileManager
import os

from kivy.config import Config
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase, DEFAULT_FONT
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
resource_add_path('fonts')
LabelBase.register(DEFAULT_FONT, 'GenShinGothic-Medium.ttf')


# GUIの立ち上げまわり
class MyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)



# 起動の宣言みたいなもの
# kivyではタイトルはAppクラスを継承したサブクラスの名のうち
# Appの前までと同じ先頭が小文字のファイル名が対応(←ク　ソ)
# MainAppの場合，main.kvが対応
class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'Data Annotator'

# Run
if __name__ == "__main__":
    MainApp().run()