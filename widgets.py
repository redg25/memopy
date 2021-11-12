from kivy.uix.button import Button
from kivy.uix.image import Image as kivImg
from typing import Optional

class Game:
    
    def __init__(self):
        self.cards: Card = []
        self.turn = Turn()

class Card(Button):
    """ Representing the state of square on the memory board.
    It can be of 4 kinds:
    - Disabled button grey background with no memory card associated.
    - Disabled button with image of memory card visible
    - Disabled button green background for found pairs
    - Enabled button with blue background for memory card to be returned face up.
    """
    def __init__(self,img:Optional[str], game):
        super().__init__()
        self.img = img
        self.found = False
        self.returned = False
        self.last_time_returned = 0  # When was the last turn where this card was returned. 0 = not returned yet
        self.game = game

    def no_card(self):
        self.background_color = [0, 0, 0, 0]
        self.text = "No card"

        self.disabled = True

    def card_face_down(self,):
        self.background_color = [0, 1, 0, 1]
        self.text = "Push me"
        self.bind(on_release=self.card_face_up)
        self.disabled = False

    def card_face_up(self,dt):
        self.widget = get_img_for_btn(self.img,self)
        self.add_widget(self.widget)
        self.disabled = True
        game_turn = self.game.turn
        if game_turn.card_returned == 0:
            game_turn.card_returned += 1
            game_turn.first_card = self
             
        elif game_turn.card_returned == 1:
            game_turn.card_returned += 1
            game_turn.second_card = self
            game_turn.first_card.remove_widget(game_turn.first_card.widget)
            game_turn.second_card.remove_widget(game_turn.second_card.widget)
            if game_turn.first_card.img == game_turn.second_card.img:
                game_turn.first_card.pair_found()
                game_turn.second_card.pair_found()
                game_turn.pair_found = True
            else:
                game_turn.first_card.card_face_down()
                game_turn.second_card.card_face_down()
            game_turn.reset_turn()

    def pair_found(self):
        self.background_color = [0, 1, 1, 1]
        self.text = "Found"
        self.disabled = False


def get_img_for_btn(img, btn):
    """
    Resize the image to fit the button
    :param img: str
    :param btn: Kivy Button object
    :return: Kivy Image object
    """
    image_path = f'images_resized/{img}'
    img_for_btn = kivImg(source=image_path,
          y=btn.y + (btn.height - btn.height / 3 * 2) / 2 ,
          x=btn.x + (btn.width - btn.width / 3 * 2) / 2,
          size=(btn.width / 3 * 2, btn.height / 3 * 2))
    return img_for_btn

class Turn:
    
    def __init__(self):
        self.player = 1
        self.card_returned = 0  # 0: no card returned, 1: one card returned, 2: both cards returned
        self.first_card = None  
        self.second_card = None
        self.pair_found = False
        
    def reset_turn(self):
        self.card_returned = 0  # 0: no card returned, 1: one card returned, 2: both cards returned
        self.first_card = None
        self.second_card = None
        self.pair_found = False
        