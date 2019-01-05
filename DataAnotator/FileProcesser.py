# -*- coding: utf-8 -*-
# FileProcesser.py
# ファイル操作に関する「処理」を記述

import os
from kivy.uix.button import Button
from kivy.app import App
from DataAnotator import Annotator


def load(path, filename):
    with open(os.path.join(path, filename[0])) as stream:
        # ロード処理
        datas = []
        for line in stream:
            line = line.strip()
            datas.append({
                "Text": line,
                "Column": line.split(","),  # 使いたい
                "Answer": -1                 # 正解
            })
        lens = len(datas)-1
        return lens, datas


def show(index, datas):
    return datas[index+1:index+11]


def save(path, filename, text):
    with open(os.path.join(path, filename), 'w') as stream:
        #セーブ処理
        stream.write(text)


def build_csv(path, filename, text):
    with open(os.path.join(path, filename), 'w') as stream:
        #書き出し処理
        stream.write(text)