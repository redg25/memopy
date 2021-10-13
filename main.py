from kivy.app import App
from memo_board import GridPageWidget


class MainApp(App):

    def build(self):
        root = GridPageWidget()
        return root

if __name__ == '__main__':
    app = MainApp()
    app.run()