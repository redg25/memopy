from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from widgets import card

class GridPageWidget(BoxLayout):

    def __init__(self,pairs=12):
        super().__init__()
        self.grid_size = pairs * 2
        self.size_grid()


    def size_grid(self):
        grids = [4, 9, 16, 25, 36, 49, 64]
        for grid in grids:
            if self.grid_size>grid:
                m_grid = int(grid**0.5)
            else:
                m_grid = int(grid**0.5)
                break

        for row in range(m_grid):
            h_layout = BoxLayout(orientation='vertical')
            for col in range(m_grid):
                button_img = card()
                button_img.no_card()
                h_layout.add_widget(button_img)
            self.add_widget(h_layout)


