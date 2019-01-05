# -*- coding: utf-8 -*-
# Annotator.py
# アノテーションエリアの処理　外部に依存まみれ

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

alphabets = [chr(i) for i in range(ord('A'), ord('Z') + 1)]


class SelectArea(GridLayout):
    def __init__(self, **kwargs):
        super(SelectArea, self).__init__(**kwargs)
        self.data = []
        self.lens = 0
        self.points = 1
        self.selects = []

    # 初回のロード
    def load_select(self, lens, datas):
        self.data = datas
        self.lens = lens
        self.points = 1
        self.show()

    def data_left(self):
        if self.points - 10 >= 1:
            self.points = self.points - 10
        elif self.points - 10 < 1:
            self.points = 1
        self.show()

    def data_right(self):
        if self.points + 10 < self.lens + 1:
            self.points = self.points + 10
        self.show()

    def show(self):
        self.ids.SelectDatas.clear_widgets()
        for i, d in enumerate(self.data[self.points:self.points + 10]):
            btn = SelectButton(text="　{}:{}".format(i + self.points,
                                alphabets[d["Answer"]] if d["Answer"] != -1 else ""),
                               index=i + self.points)
            self.ids.SelectDatas.add_widget(btn)

    def data_select(self, index):
        a_area = self.parent.children[0]
        a_area.show_text(self.data[index])
        a_area.show_selects(index)

    def answer(self, index, answer):
        self.data[index]["Answer"] = answer
        self.show()
        self.data_select(index+1 if index<self.lens else index)


class SelectButton(Button):
    index = ObjectProperty(None)

    def show(self, ix):
        self.parent.parent.parent.data_select(ix)


class AnnotateArea(GridLayout):
    def __init__(self, **kwargs):
        super(AnnotateArea, self).__init__(**kwargs)

    def show_text(self, d):
        self.ids.showArea.clear_widgets()
        # ここに表示内容の処理
        label = ShowText(text=d["Text"])
        self.ids.showArea.add_widget(label)

    def show_selects(self, index):
        self.ids.pressArea.clear_widgets()
        for i, tup in enumerate(zip(alphabets, self.parent.children[1].selects)):
            a, s = tup[0], tup[1]
            btn = AnswerButton(text=" {}:{}".format(a, s), answer=i, index=index)
            self.ids.pressArea.add_widget(btn)
        btn = CreateAnswerButton(text=" 1:新しく選択肢をつくる", index=index)
        self.ids.pressArea.add_widget(btn)


class CreateAnswerButton(Button):
    index = ObjectProperty(None)

    def add_answers(self, index):
        App.get_running_app().root.children[0].children[1].selects.append("新しい選択肢")
        self.parent.parent.parent.show_selects(index)


class AnswerButton(Button):
    index = ObjectProperty(None)
    answer = ObjectProperty(None)

    def put_answer(self, ix, ans):
        App.get_running_app().root.children[0].children[1].answer(ix, ans)


class ShowText(Label):
    pass
