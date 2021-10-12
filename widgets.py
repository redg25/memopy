from kivy.uix.button import Button

class card(Button):

    def no_card(self):
        self.background_color = [0, 0, 0, 0]
        self.text = "None"
        self.disabled = True


    def with_image(self):
        self.background_color = [0, 1, 0, 1]
        self.text = "Push"
        self.disabled = False
