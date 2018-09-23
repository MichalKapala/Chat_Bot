from kivy.config import Config
Config.set('graphics', 'resizable', False)
#Config.set('graphics','fullscreen', True)
from kivy.uix.listview import ListView
from kivy.uix.floatlayout import FloatLayout
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.uix.label import Label
from kivy.animation import Animation as anim
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition
import kivy
import chat
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from time import sleep
import texts

Window.size = (450, 575)
Window.softinput_mode = 'pan'
Builder.load_file('main.kv')
kivy.require('1.10.0')


class ImageButton(ButtonBehavior, Image):
    def __init__(self, number=None,  **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.number1 = number


class CustomLabel(Label):
    pass


class Input(TextInput):
    pass


class List(ListView):
    pass

class Profile(Screen):
    def __init__(self,tytul, przedmioty, jobcy, cklasy,  **kwargs):
        super(Profile, self).__init__(**kwargs)
        self.tytul = tytul
        self.przedmioty = przedmioty
        self.jobcy = jobcy
        self.cklasy=cklasy



class ChatScreen(Screen):
    def __init__(self, **kwargs):
        self.name = 'chat'
        super(ChatScreen, self).__init__(**kwargs)
        self.lab = MainView()
        self.add_widget(self.lab)


class MenuScreen(Screen):
    pass


class DateScreen(Screen):
    pass


class ContactScreen(Screen):
    pass


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.size = Window.size

        self.ek_nazwa = ["bio", "mat", "geo", "biotech", "human"]

        self.s = [(Window.width * 0.5, self.height * 0.91 * 0.5),
                  (Window.width * 0.5, self.height * 0.91 * 0.5),
                  (Window.width * 0.5, self.height * 0.91 * 0.3333),
                  (Window.width * 0.5, self.height * 0.91 * 0.3333),
                  (Window.width * 0.5, self.height * 0.91 * 0.3333)
                  ]
        self.p = [(0, Window.height * 0.09),
                  (0, Window.height * 0.09 + self.height * 0.91 * 0.5),
                  (Window.width * 0.5, Window.height * 0.09),
                  (Window.width * 0.5, Window.height * 0.09 + self.height * 0.91 * 0.3333),
                  (Window.width * 0.5, Window.height * 0.09 + self.height * 0.91 * 0.3333 * 2)
                  ]

        argumenty = {
            'allow_stretch': True,
            'keep_ratio': False,
            'size_hint_x': None,
            'size_hint_y': None
        }

        self.lay = FloatLayout(pos=(0, Window.height*0.09), size_hint=(1, 0.91))
        self.add_widget(self.lay)

        self.bio = ImageButton(
                               number=1,
                               source='Grafika/bio.png',
                               size=self.s[0],
                               pos=self.p[0],
                               **argumenty)
        self.bio.bind(on_press=self.animate)

        self.mat = ImageButton(
                               number=2,
                               source='Grafika/mat.png',
                               size=self.s[1],
                               pos=self.p[1],
                               **argumenty)
        self.mat.bind(on_press=self.animate)

        self.geo = ImageButton(
                               number=3,
                               source='Grafika/geo.png',
                               size=self.s[2],
                               pos=self.p[2],
                               **argumenty)
        self.geo.bind(on_press=self.animate)

        self.biotech = ImageButton(
                               number=4,
                               source='Grafika/biotech.png',
                               size=self.s[3],
                               pos=self.p[3],
                               **argumenty)
        self.biotech.bind(on_press=self.animate)

        self.human = ImageButton(
                                number=5,
                                source='Grafika/human.png',
                                size=self.s[4],
                                pos=self.p[4],
                                **argumenty)
        self.human.bind(on_press=self.animate)

        self.lay.add_widget(self.bio)
        self.lay.add_widget(self.mat)
        self.lay.add_widget(self.geo)
        self.lay.add_widget(self.biotech)
        self.lay.add_widget(self.human)
        print(self.transition_state)

    def animate(self, obj):
        self.lay.remove_widget(obj)
        self.lay.add_widget(obj)
        animation = anim(x=Window.width / 2 - obj.width / 2, y=Window.height*0.91 / 2 - obj.height / 2, transition='in_out_back')
        animation += anim(size=self.lay.size, duration=0.75) & anim(x=0, y=Window.height * 0.09, duration= 0.75)
        animation.start(obj)

        animation.bind(on_complete=self.koniec_animacji)

    def koniec_animacji(self, obj, obj1):
        print(self.transition_progress)
        sleep(1)
        sm.current = self.ek_nazwa[obj1.number1-1]
        if self.transition_progress == 0:
            obj1.size = self.s[obj1.number1 - 1]
            obj1.pos = self.p[obj1.number1 - 1]


class MainView(FloatLayout):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.size = (Window.width, Window.height)
        self.adapter = SimpleListAdapter(data=[" "], cls=CustomLabel, args_converter=self.list_item_args_converter)
        self.adapter.data.append("Franek: Witaj, jak mogę cie pomóc?")
        self.list_view = List(adapter=self.adapter)
        self.inp = Input(is_focusable=True)

        self.add_widget(self.list_view)
        self.add_widget(self.inp)
        self.i = 0
        self.inp.bind(on_text_validate=self.click)

    def click(self, obj = None):
        self.i += 1
        pytanie = self.inp.text
        self.adapter.data.append('Ty: '+pytanie)
        odpowiedz = chat.Chat().odpowiedz(pytanie)
        self.adapter.data.append('Franek: ' + odpowiedz)
        if self.i >= 6:
            self.list_view.scroll_to((self.i*2)-9)
        self.inp.text = ""

    def zmiana(self):
        sm.current = 'menu'

    def list_item_args_converter(self, col, obj):
        return{
            'text':obj,
            'height': 50
        }

mat=Profile(name='mat', tytul=texts.mat[0], przedmioty=texts.mat[1], jobcy=texts.mat[2], cklasy=texts.mat[3])
bio=Profile(name='bio', tytul=texts.biol[0], przedmioty=texts.biol[1], jobcy=texts.biol[2],cklasy=texts.biol[3])
geo=Profile(name='geo', tytul=texts.geo[0], przedmioty=texts.geo[1], jobcy=texts.geo[2], cklasy=texts.geo[3])
biotech=Profile(name="biotech", tytul=texts.biot[0], przedmioty=texts.biot[1], jobcy=texts.biot[2], cklasy=texts.biot[3])
human=Profile(name='human', tytul=texts.human[0], przedmioty=texts.human[1], jobcy=texts.human[2], cklasy=texts.biot[3])
sm = ScreenManager(transition=NoTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(ChatScreen())
sm.add_widget(DateScreen(name='date'))
sm.add_widget(ContactScreen(name='contact'))
sm.add_widget(mat)
sm.add_widget(bio)
sm.add_widget(geo)
sm.add_widget(biotech)
sm.add_widget(human)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(sm)

