# -*- coding: utf-8 -*-
# FileProcesser.py
# ファイル操作に関する「処理」を記述

import os


def load(path, filename):
    with open(os.path.join(path, filename[0])) as stream:
        # ロード処理
        print(stream.read())


def save(path, filename, text):
    with open(os.path.join(path, filename), 'w') as stream:
        #セーブ処理
        stream.write(text)


def build_csv(path, filename, text):
    with open(os.path.join(path, filename), 'w') as stream:
        #書き出し処理
        stream.write(text)