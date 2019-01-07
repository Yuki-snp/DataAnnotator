# -*- coding: utf-8 -*-
# Annotator.py
# アノテーションエリアの処理　外部に依存まみれ

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder

alphabets = [chr(i) for i in range(ord('A'), ord('Z') + 1)]


class MainArea(BoxLayout):
    pass


class SelectArea(GridLayout):
    def __init__(self, **kwargs):
        super(SelectArea, self).__init__(**kwargs)
        self.data = []
        self.lens = 0
        self.points = 1
        self.selects = []
        self.now_select = 1
        self.data_type = ".txt"

    # 初回のロード
    def load_select(self, lens, datas, selects):
        self.data = datas
        self.lens = lens
        self.points = 1
        self.selects = selects
        self.now_select = 1
        self.data_select(self.now_select)

    def data_left(self):
        if self.points - 10 >= 1:
            self.points = self.points - 10
            self.now_select = self.points
        elif self.points - 10 < 1:
            if self.points != 1:
                self.now_select = self.points
            self.points = 1
        self.data_select(self.now_select)

    def data_right(self):
        if self.points + 10 < self.lens + 1:
            self.points = self.points + 10
            self.now_select = self.points
        self.data_select(self.now_select)

    def show(self):
        self.ids.SelectDatas.clear_widgets()
        for i, d in enumerate(self.data[self.points:self.points + 10]):
            btn = SelectButton(text="　{}:{}".format(i + self.points,
                                alphabets[d["Answer"]] if d["Answer"] != -1 else ""),
                               index=i + self.points,
                               background_color=(0, .6, .9, 1) if i+self.points==self.now_select else (.8, .8, .8, 1))
            self.ids.SelectDatas.add_widget(btn)

    def data_select(self, index):
        if len(self.data) == 0: return
        self.now_select = index
        a_area = self.parent.children[0]
        a_area.show_text(self.data[index], self.data[0])
        a_area.show_selects(index)
        self.show()

    def answer(self, index, answer):
        self.data[index]["Answer"] = answer
        if answer != -1:
            self.data_select(index + 1 if index < self.lens else index)
            if index+1 >= self.points + 10:
                self.data_right()
        else:
            self.show()


class SelectButton(Button):
    index = ObjectProperty(None)

    def show(self, ix):
        self.parent.parent.parent.data_select(ix)


class AnnotateArea(GridLayout):
    def __init__(self, **kwargs):
        super(AnnotateArea, self).__init__(**kwargs)

    def show_text(self, d, column):
        self.ids.showArea.clear_widgets()
        # ここに表示内容の処理
        label = ShowText(text=column["Text"]+"\n"+d["Text"])
        self.ids.showArea.add_widget(label)

    def show_selects(self, index):
        self.ids.pressArea.clear_widgets()
        for i, tup in enumerate(zip(alphabets, self.parent.children[1].selects)):
            a, s = tup[0], tup[1]
            btn = AnswerButton(text=" {}:{}".format(a, s), answer=i, index=index)
            self.ids.pressArea.add_widget(btn)

        if len(self.parent.children[1].selects)<26:
            btn = CreateAnswerButton(text=" 1:新しく選択肢を作成する", index=index)
            self.ids.pressArea.add_widget(btn)

        btn = AnswerButton(text=" 2:選択をはずす", answer=-1, index=index)
        self.ids.pressArea.add_widget(btn)


class CreateAnswerButton(Button):
    index = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CreateAnswerButton, self).__init__(**kwargs)

    def dismiss_popup(self):
        self._popup.dismiss()

    def add_answers(self, index):
        #ここにpopup処理を書く
        content = CreateAnswerDialog(make=self.make_answer, cancel=self.dismiss_popup, index=index)
        self._popup = Popup(title="新しく選択肢を作成する", content=content,
                            size_hint=(0.5, None), size=(300,120))
        self._popup.open()

    def make_answer(self, index, text):
        App.get_running_app().root.children[0].children[1].selects.append(text)
        self.parent.parent.parent.show_selects(index)
        self.dismiss_popup()


class CreateAnswerDialog(FloatLayout):
    index = ObjectProperty(None)
    make = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class AnswerButton(Button):
    index = ObjectProperty(None)
    answer = ObjectProperty(None)

    def put_answer(self, ix, ans):
        App.get_running_app().root.children[0].children[1].answer(ix, ans)


class ShowText(Label):
    pass
