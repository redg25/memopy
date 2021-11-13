from kivy.uix.button import Button
from kivy.uix.image import Image as kivImg
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from PIL import Image as PilImg
from typing import Optional

class Game:
    
    def __init__(self, players: int = 2):
        self.players = players
        self.cards: Card = []
        self.turn = Turn()
        self.scores = {'1': 0, '2': 0}
        self.pairs = None

    def set_next_turn(self):
        # reset turn
        self.turn.first_card = None
        self.turn.second_card = None
        self.turn.card_returned = 0
        # player found a pair, adds one the player's score
        if self.turn.pair_found:
            self.scores[str(self.turn.player)] += 1
            print(self.scores)
            self.turn.pair_found = False
        # player 1 fails to find a pair
        elif self.turn.player == 1 and self.players ==2:
            self.turn.player = 2
            print(self.scores)
        # player 2 fails to find a pair
        elif self.turn.player == 2 and self.players ==2:
            self.turn.player = 1
            print(self.scores)
           

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
        self.img: str = img  # file name of image
        self.found = False
        self.returned = False
        self.last_time_returned = 0  # When was the last turn where this card was returned. 0 = not returned yet
        self.game: Game = game
        self.background_color = [0, 0, 0, 0]
        self.text: str = ""
        self.disabled = True
        self.img_widget: kivImg = None

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
        card_pop_up(self.img)
        self.img_widget = get_img_for_btn(self.img, self)
        self.add_widget(self.img_widget)
        self.disabled = True
        game_turn = self.game.turn
        if game_turn.card_returned == 0:
            game_turn.card_returned += 1
            game_turn.first_card = self
             
        elif game_turn.card_returned == 1:
            game_turn.card_returned += 1
            game_turn.second_card = self
            game_turn.first_card.remove_widget(game_turn.first_card.img_widget)
            game_turn.second_card.remove_widget(game_turn.second_card.img_widget)
            if game_turn.first_card.img == game_turn.second_card.img:
                game_turn.first_card.pair_found()
                game_turn.second_card.pair_found()
                game_turn.pair_found = True
            else:
                game_turn.first_card.card_face_down()
                game_turn.second_card.card_face_down()
            self.game.set_next_turn()

    def pair_found(self):
        self.background_color = [0, 1, 1, 1]
        self.text = "Found"
        self.disabled = False


def card_pop_up(img):
    """Open a full screen pop up with the image on the card
     When the user clicks anywhere the pop up disappears
     """
    resized_img = PilImg.open('images_resized/' + img)
    size_of_image = resized_img.size
    ratio = size_of_image[0] / size_of_image[1]
    pop_up_size = (500 * ratio, 500)
    pop_up = ModalView(background='images_resized/' + img, size_hint=(None, None), size=pop_up_size,
                         auto_dismiss=False)
    pop_up.bind(on_touch_down=pop_up.dismiss)
    pop_up.open()
    
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
        self.player: int = 1  # Player's turn. 1 or 2. 
        self.card_returned: int = 0  # 0: no card returned, 1: one card returned, 2: both cards returned
        self.first_card: Card = None  
        self.second_card: Card = None
        self.pair_found = False



            
            
        