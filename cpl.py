from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import datetime


# ID Number Masking
class IDInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        if substring.isdigit() != True:
            substring = substring[0:-1]
        elif (len(self.text) > 5):
            substring = substring[0:-1]
        return super(IDInput, self).insert_text(substring, from_undo=from_undo)


class LoginScreen(GridLayout):
    # Writing
    def Add(self, *args):
        if (len(str(self.username.text)) == 6):
            s = str(self.username.text) + ',' + str(datetime.now()) + '\n'
            f = open('Data.csv', 'a')
            f.write(s)
            self.username.text = ''

    # Button Layout
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        drop = DropDown()
        self.add_widget(Label(text='ID Number'))
        self.username = IDInput(multiline=False)
        self.add_widget(self.username)
        mainbut = Button(text='Lab', size_hint_y=None, height=50)
        mainbut.bind(on_release=drop.open)
        self.add_widget(Label(text='Location'))
        self.add_widget(mainbut)
        labut = Button(text='Lab', size_hint_y=None, height=50)
        clabut = Button(text='Classroom', size_hint_y=None, height=50)
        stubut = Button(text='Studio', size_hint_y=None, height=50)
        conbut = Button(text='Consultation ', size_hint_y=None, height=50)
        wsbut = Button(text='Work Study', size_hint_y=None, height=50)
        labut.bind(on_release=lambda labut: drop.select(labut.text))
        clabut.bind(on_release=lambda clabut: drop.select(clabut.text))
        stubut.bind(on_release=lambda stubut: drop.select(stubut.text))
        conbut.bind(on_release=lambda conbut: drop.select(conbut.text))
        wsbut.bind(on_release=lambda wsbut: drop.select(wsbut.text))
        drop.bind(on_select=lambda instance, x: setattr(mainbut, "text", x))
        drop.add_widget(labut)
        drop.add_widget(clabut)
        drop.add_widget(stubut)
        drop.add_widget(conbut)
        drop.add_widget(wsbut)
        button = Button(text='Submit', size_hint_y=None, height=50)
        button.bind(on_release=self.Add)
        self.add_widget(button)


# Rebuilding
class MyApp(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
