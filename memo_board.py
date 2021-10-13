from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from widgets import card

class GridPageWidget(BoxLayout):

    def __init__(self,pairs=12):
        super().__init__()
        self.grid_size = pairs * 2
        self.draw_grid()


    def draw_grid(self):
        
        # Using a list of possible grid sizes,
        # calculate the size needed based on the number of pairs
        # Ex: If 10 pairs, we need 20 cards that will fit in a 25 squares grid.
        grids = [4, 9, 16, 25, 36, 49, 64]
        max_grid = [int(grids[i+1] **0.5) for i, x in enumerate(grids)
                if (self.grid_size> x and self.grid_size <grids[i+1])][0]

        cards = []

        for row in range(max_grid):
            h_layout = BoxLayout(orientation='vertical')
            for col in range(max_grid):
                button_img = card('images/img1.jpg')
                #button_img.no_card()
                #button_img.pair_found()
                button_img.card_face_down()
                cards.append(button_img)
                h_layout.add_widget(button_img)
            self.add_widget(h_layout)
        for mame in cards:
            print (mame)



