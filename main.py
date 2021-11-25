from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
import os, shutil, random
from PIL import Image,ExifTags
from kivy.uix.button import Button
from kivy.uix.image import Image as kivImg
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.lang import Builder
from PIL import Image as PilImg
from typing import Optional
import json


class FirstPageWidget(BoxLayout):

    def game_parameters(self):

        def toggle_choice(choices):
            for choice in choices:
                if choice.state == 'down':
                    return choice.text

        pairs = int(toggle_choice(self.children[3].children))
        if toggle_choice(self.children[1].children) == '1P':
            nb_player = 1
        else: nb_player = 2
        root.clear_widgets()
        root.add_widget(GamePage(nb_player, pairs))


    def get_default_path(self):
        self.path = os.path.expanduser("~/Desktop")
        return self.path

    def get_saved_folder(self):
        with open('config.json','r') as f:
            data = json.load(f)
        folder_path = data['settings']['folder_path']
        folder_name = data['settings']['folder_name']
        return folder_path, folder_name

    def update_folder_label(self, widget, text):
        with open('config.json','r') as f:
            data = json.load(f)
        folder_path = f'{text[0]}\\'
        folder_name = text[0].split('\\')[-1]
        data['settings']['folder_path'] = folder_path
        data['settings']['folder_name'] = folder_name
        with open('config.json','w') as f:
            json.dump(data, f)
        if os.path.isdir(folder_path):
            widget.text = folder_name
            widget.color = [1,1,1,1]
        else:
            widget.text = 'Please select a directory'
            widget.color = [1,0,0,1]



class GamePage(BoxLayout):

    def __init__(self,  players: int, pairs: int):
        super().__init__()

        self.game = Game(pairs,players)
        h_layout = BoxLayout(orientation='vertical')
        grid = GridPageWidget( self.game,pairs)

        h_layout.add_widget(grid)
        scores_layout = BoxLayout(orientation='horizontal',size_hint_y = 0.2)
        for player in range(1,players+1):
            player_lbl = Label(text= f'Player {str(player)}')
            score_lbl = Label(text= '0')
            self.game.scores[str(player)]['widget'] = score_lbl
            self.game.scores[str(player)]['label'] = player_lbl
            scores_layout.add_widget(player_lbl)
            scores_layout.add_widget(score_lbl)
        h_layout.add_widget(scores_layout)
        self.add_widget(h_layout)
        if players == 2:
            self.game.scores['1']['label'].color = [0,0.6,0,1]
            self.game.scores['1']['label'].font_size = 20




class GridPageWidget(BoxLayout):

    def __init__(self,  game, pairs: int):
        super().__init__()
        self.game = game
        self.pairs = pairs
        self.grid_size = pairs * 2
        self.pool_of_cards = []
        self.select_pictures()

    def select_pictures(self):
        if platform == 'android':
            self.folder = '/sdcard/DCIM/Camera/'
        else:
            self.folder = root.get_saved_folder()[0]

        for filename in os.listdir('images_resized'):
            file_path = os.path.join('images_resized', filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        pic_folder = os.listdir(self.folder)
        pic_folder = [x for x in pic_folder if x[-4:].lower() == '.jpg']
        if len(pic_folder)<=self.pairs:
            #write function to change size
            pass

        nb_of_pairs_created = 0
        self.i = 0

        while nb_of_pairs_created < self.pairs:
            pick = random.choice(pic_folder)
            if pick not in self.pool_of_cards and pick[-4:].lower()=='.jpg':
                self.pool_of_cards.append(pick)
                nb_of_pairs_created += 1
        self.pb = progress_bar_func(self.pairs,'Please wait. Pictures are being selected and resized',self.resize_and_save_pictures)

    def resize_and_save_pictures(self, dt):
            if self.i<self.pairs:
                print(f'saving {self.pool_of_cards[self.i]}...')
                img = Image.open(self.folder + self.pool_of_cards[self.i])
                # Get Image orientation
                exif = img._getexif()
                for tag, value in exif.items():
                    decoded = ExifTags.TAGS.get(tag, tag)
                    if decoded == 'Orientation':
                        print(value)
                        if value == 6:
                            print(f'{self.pool_of_cards[self.i]} is vertical')
                            img = img.transpose(Image.ROTATE_270)
                        elif value == 8:
                            print(f'{self.pool_of_cards[self.i]} is vertical')
                            img = img.transpose(Image.ROTATE_90)
                img.save("images_resized/" + self.pool_of_cards[self.i], quality=95)
                # print(f'{[self.image_selection[self.i]]} is saved')
                self.pb.progress_bar.value += 1

                self.pb.trigger()
                self.i += 1
            else:
                self.pb.popup.dismiss()
                self.pool_of_cards = [val for val in self.pool_of_cards for _ in (0, 1)]
                self.draw_grid()


    def draw_grid(self):
        """
        Using a list of possible grid sizes,
        calculate the size needed based on the number of pairs
        Ex: If 10 pairs, we need 20 cards that will fit in a 25 squares grid.
        """

        #self.select_pictures()

        grids = [4, 9, 16, 25, 36, 49, 64]
        max_grid = [int(grids[i+1] ** 0.5) for i, x in enumerate(grids)
                    if (self.grid_size > x and self.grid_size <= grids[i+1])][0]

        #cards = []

        for row in range(max_grid):
            h_layout = BoxLayout(orientation='vertical')
            for col in range(max_grid):
                try:
                    i = random.randrange(len(self.pool_of_cards))
                    img = self.pool_of_cards.pop(i)
                    button_img = Card(img, self.game)
                    #button_img.no_card()
                    #button_img.pair_found()
                    button_img.card_face_down()
                    #cards.append(button_img)
                    h_layout.add_widget(button_img)
                except:
                    button_img = Card(None, self.game)
                    button_img.no_card()
                    #self.game.cards.append(button_img)
                    h_layout.add_widget(button_img)
            self.add_widget(h_layout)
            turn = Turn()
        # for mame in cards:
        #     print (mame)

class progress_bar_func():

    def __init__(self,maxi,label,event):
        self.progress_bar = ProgressBar(max=maxi)
        self.popup = Popup(title=label,
                           content=self.progress_bar)
        self.trigger = Clock.create_trigger(event)
        self.popup.open()
        self.popup.bind(on_open=event)
        self.progress_bar.value = 1


class Game:

    def __init__(self,  pairs: int, players: int):
        self.players = players
        # self.cards: Card = []
        self.turn = Turn()
        self.scores = {'1': {'score':0,'widget':None,'label':None}, '2': {'score':0,'widget':None,'label':None}}
        self.pairs_found = 0
        self.pairs = pairs

    def set_next_turn(self):

        # reset turn
        self.turn.first_card = None
        self.turn.second_card = None
        self.turn.card_returned = 0
        player = str(self.turn.player)
        # player found a pair, adds one the player's score
        if self.turn.pair_found:
            self.pairs_found +=1
            self.scores[player]['score'] += 1
            self.scores[player]['widget'].text = str(self.scores[player]['score'])
            print(self.scores)
            self.turn.pair_found = False
            if self.pairs_found == self.pairs:
                root.clear_widgets()
                root.add_widget(end_screen(player))
        # player 1 fails to find a pair
        elif self.turn.player == 1 and self.players ==2:
            self.turn.player = 2
            print(self.scores)
            print (f'change of player, now {str(self.turn.player)}')
        # player 2 fails to find a pair
        elif self.turn.player == 2 and self.players ==2:
            self.turn.player = 1
            print (f'change of player, now {str(self.turn.player)}')
            print(self.scores)
        if self.players ==2:
            for p in self.scores:
                if p == str(self.turn.player):
                    self.scores[p]['label'].color = [0,0.6,0,1]
                    self.scores[p]['label'].font_size = 20
                else:
                    self.scores[p]['label'].color = [1,1,1,1]
                    self.scores[p]['label'].font_size = 16


def end_screen(winner):
    h_layout = BoxLayout(orientation='vertical')
    winner = Label(text=f'Player {winner} wins the game')
    w_layout = BoxLayout(orientation='horizontal')
    btn_new_game = Button(text='New Game', on_release=new_game)
    btn_close_game = Button(text='Close', on_release=app.stop)
    w_layout.add_widget(btn_new_game)
    w_layout.add_widget(btn_close_game)
    h_layout.add_widget(winner)
    h_layout.add_widget(w_layout)
    return h_layout


def new_game(dt):
    root.clear_widgets()
    root.add_widget(FirstPageWidget())


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
        self.disabled = True


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






class MainApp(App):

    def build(self):
        global root
        root = FirstPageWidget()
        return root



if __name__ == '__main__':
    app = MainApp()
    app.run()