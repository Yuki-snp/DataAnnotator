# -*- coding: utf-8 -*-
# FileManager.py
# file.kv読み込み
# ファイル操作に関する「操作」を記述

from kivy.uix.actionbar import ActionGroup
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from DataAnotator import FileProcesser
import os
Builder.load_file('file.kv')


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class FileManager(ActionGroup):
    path = os.environ["HOME"]

    def __init__(self, **kwargs):
        super(FileManager, self).__init__(**kwargs)

    # ポップアップの削除
    def dismiss_popup(self):
        self._popup.dismiss()

    # ポップアップの呼出(ボタンが押された時の動作)
    def file_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="読み込む", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    # データをロードする時の動作
    def load(self, path, filename):
        if filename:
            if os.path.splitext(filename)[1] in ["txt", "csv"]:
                FileProcesser.load(path, filename)
            else:
                #非対応のファイルです
            self.dismiss_popup()

    # 保存
    def file_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="保存", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        if filename!="":
            FileProcesser.save(path, filename, self.text_input.text)
            self.dismiss_popup()

    # 書き出し
    def file_build_csv(self):
        content = SaveDialog(save=self.build_csv, cancel=self.dismiss_popup)
        self._popup = Popup(title="書き出し", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def build_csv(self, path, filename):
        if filename != "":
            FileProcesser.bulid_csv(path, filename, self.text_input.text)
            self.dismiss_popup()