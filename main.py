from kivy.app import App
from memo_board import GridPageWidget, GamePage, FirstPageWidget
from kivy.uix.boxlayout import BoxLayout




class MainApp(App):

    def build(self):
        global root
        root = FirstPageWidget()
        return root

if __name__ == '__main__':
    app = MainApp()
    app.run()