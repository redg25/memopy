from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from widgets import card
from kivy.utils import platform
import os, shutil, random
from PIL import Image,ExifTags

class GridPageWidget(BoxLayout):

    def __init__(self,pairs=12):
        super().__init__()
        self.pairs = pairs
        self.grid_size = pairs * 2
        self.pool_of_cards = []
        self.draw_grid()


    def select_pictures(self):
        if platform == 'android':
            self.folder = '/sdcard/DCIM/Camera/'
        else:
            self.folder = 'C:\\Users\\regis\\My_folder\\Pictures\\Camera Back up 20201224\\'

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

        i = 0
        while i < self.pairs:
            pick = random.choice(pic_folder)
            if pick not in self.pool_of_cards and pick[-4:].lower()=='.jpg':
                self.pool_of_cards.append(pick)
                self.get_picture_from_phone(pick)
                i+=1
        #self.pb = progress_bar_func(self.size_game,'Please wait. Pictures are being selected and resized',self.get_picture_from_phone)

    def get_picture_from_phone(self, pic):

        print(f'saving {pic}...')
        foo = Image.open(self.folder + pic)
        # Get Image orientation
        exif = foo._getexif()
        for tag, value in exif.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            if decoded == 'Orientation':
                print(value)
                if value == 6:
                    print(f'{pic} is vertical')
                    foo = foo.transpose(Image.ROTATE_270)
                elif value == 8:
                    print(f'{pic} is vertical')
                    foo = foo.transpose(Image.ROTATE_90)
        foo.save("images_resized/" + pic, quality=95)
        # print(f'{[self.image_selection[self.i]]} is saved')
        # self.i += 1
        # self.pb.progress_bar.value += 1
        # self.pb.trigger()
    # else:
    #     self.pb.popup.dismiss()
    #     self.create_grid()

    def draw_grid(self):
        
        # Using a list of possible grid sizes,
        # calculate the size needed based on the number of pairs
        # Ex: If 10 pairs, we need 20 cards that will fit in a 25 squares grid.

        self.select_pictures()

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



