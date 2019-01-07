# -*- coding: utf-8 -*-
# FileManager.py
# file.kv読み込み
# ファイル操作に関する「操作」を記述

from kivy.uix.actionbar import ActionGroup
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from DataAnnotator import FileProcesser
from kivy.app import App
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
            s_area = App.get_running_app().root.children[0].children[1]
            if os.path.splitext(filename[0])[1] in [".txt", ".csv"]:
                lens, datas = FileProcesser.load(path, filename)
                s_area.load_select(lens, datas, [])
                self.dismiss_popup()
            elif os.path.splitext(filename[0])[1] in [".dant"]:
                lens, datas, selects = FileProcesser.load_dant(path, filename)
                s_area.load_select(lens, datas, selects)
                self.dismiss_popup()
            else:
                # 非対応のファイルです
                content = Label(text="非対応のファイルです")
                App.get_running_app().root._popup = Popup(title="FileLoadError!", content=content,
                                    size_hint=(None, None), size=(200, 100) )
                App.get_running_app().root._popup.open()

    # 作業中データの保存
    def file_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="一時保存", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        if filename!="":
            if filename[-5:] != ".dant":
                filename += ".dant"
            s_area = App.get_running_app().root.children[0].children[1]
            data = s_area.data
            answers = s_area.selects
            FileProcesser.save(path, filename, data, answers)
            self.dismiss_popup()

    # ファイル書き出し
    def file_build_csv(self):
        content = SaveDialog(save=self.build_csv, cancel=self.dismiss_popup)
        self._popup = Popup(title="書き出す", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def build_csv(self, path, filename):
        if filename != "":
            if filename[-4:] != ".csv":
                filename += ".csv"
            s_area = App.get_running_app().root.children[0].children[1]
            data = s_area.data
            answers = s_area.selects
            FileProcesser.build_csv(path, filename, data, answers)
            self.dismiss_popup()