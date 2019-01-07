# -*- coding: utf-8 -*-
# FileProcesser.py
# ファイル操作に関する「処理」を記述

import os
from kivy.uix.button import Button
from kivy.app import App
from DataAnnotator import Annotator


def load(path, filename):
    with open(os.path.join(path, filename[0])) as stream:
        # ロード処理
        datas = []
        for line in stream:
            line = line.strip()
            datas.append({
                "Text": line,
                "Column": line.split(","),  # 使いたい
                "Answer": -1  # 正解
            })
        lens = len(datas) - 1
        return lens, datas


def load_dant(path, filename):
    with open(os.path.join(path, filename[0])) as stream:
        # ロード処理
        datas = []
        selects = []
        load_level = 0
        ix = 0
        for line in stream:
            line = line.strip()
            if line == "---data_anotator---":
                load_level += 1
            elif load_level==0: # 選択肢
                selects.append(line)
            elif load_level==1: # データ
                datas.append({
                    "Text": line,
                    "Column": line.split(","),  # 使いたい
                })
            elif load_level==2: # 正解
                datas[ix]["Answer"] = int(line)
                ix += 1
        lens = len(datas) - 1
        return lens, datas, selects


def save(path, filename, data, answers):
    with open(os.path.join(path, filename), 'w') as stream:
        # セーブ処理
        for a in answers:
            stream.write(a+"\n")
        stream.write("---data_anotator---\n")

        for d in data:
            stream.write(d["Text"] + "\n")
        stream.write("---data_anotator---\n")

        for d in data:
            stream.write(str(d["Answer"]) + "\n")


def build_csv(path, filename, data, answers):
    with open(os.path.join(path, filename), 'w') as stream:
        # 書き出し処理
        for i, d in enumerate(data):
            text = d["Text"]
            if i == 0:
                text += "," + "Answer"
            else:
                ans = answers[d["Answer"]] if d["Answer"] != -1 else ""
                text += "," + ans
            stream.write(text + "\n")
