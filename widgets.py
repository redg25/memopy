from kivy.uix.button import Button
from kivy.uix.image import Image as kivImg

class card(Button):
    """ Representing the state of square on the memory board.
    It can be of 4 kinds:
    - Disabled button grey background with no memory card associated.
    - Disabled button with image of memory card visible
    - Disabled button green background for found pairs
    - Enabled button with blue background for memory card to be returned face up.
    """
    def __init__(self,img):
        super().__init__()
        self.img = img

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
        widget = get_img_for_btn(self.img,self)
        self.add_widget(widget)
        self.disabled = True

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
    img_for_btn = kivImg(source=img,
          y=btn.y + (btn.height - btn.height / 3 * 2) / 2 ,
          x=btn.x + (btn.width - btn.width / 3 * 2) / 2,
          size=(btn.width / 3 * 2, btn.height / 3 * 2))
    return img_for_btn