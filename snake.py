from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from random import randint
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty
from kivy.core.window import Window

class SnakePart(Widget):
    pass

class GameScreen(Widget):
    number = NumericProperty()
    step_size= 40
    movement_x= 0
    movement_y= 0
    snake_parts= []

    def __init__(self,**kwargs):
        super(GameScreen,self).__init__(**kwargs)
        Clock.schedule_interval(self.increment_time, .1)
        self.increment_time(.25)

    def new_game(self):
        to_be_removed = []
        for child in self.children:
            if isinstance(child, SnakePart):
                to_be_removed.append(child)
        for child in to_be_removed:
            self.remove_widget(child)

            
        self.snake_parts = []
        self.movement_x = 0
        self.movement_y = 0
        head= SnakePart()
        head.pos=(0,0)
        self.snake_parts.append(head)
        self.add_widget(head)


    def on_touch_up(self, touch):
        dx = touch.x-touch.opos[0]
        dy = touch.y-touch.opos[1]
        if abs(dx)>abs(dy):
            #Moving left or right
            self.movement_y=0
            if dx>0:
                self.movement_x = self.step_size
            else:
                self.movement_x = -self.step_size
        else:
            #moving up or down
            self.movement_x=0
            if dy>0:
                self.movement_y = self.step_size
            else:
                self.movement_y = -self.step_size

    def collides_widget(self,wid1,wid2):
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True

    def increment_time(self, interval):
        self.number += .1

    def start(self):
        Clock.unschedule(self.increment_time)
        Clock.schedule_interval(self.increment_time, .1)
        

    def next_frame(self, *args):
        
        #Move the snake
        head = self.snake_parts[0]
        food = self.ids.food
        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y


        # Move the body
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            part.new_y = self.snake_parts[i-1].y
            part.new_x = self.snake_parts[i-1].x
        for part in self.snake_parts[1:]:
            part.y = part.new_y
            part.x = part.new_x

        # Move the Head
        head.x += self.movement_x
        head.y += self.movement_y




        #Check for snake colliding with food
        if self.collides_widget(head, food):
            Clock.schedule_interval(self.increment_time, .1)
            food.x = randint(0,Window.width-food.width)
            food.y = randint(0,Window.height-food.height)
            new_part= SnakePart()
            new_part.x=last_x
            new_part.y=last_y
            self.snake_parts.append(new_part)
            self.add_widget(new_part)
        #Check for snake colliding with snake
        for part in self.snake_parts[1:]:
            if self.collides_widget(part, head):
                c=Label(text="Game Over")
                popup=Popup(title='Snake Mania',content=c,size_hint=(None, None),size=(400,400),auto_dismiss=True)
                popup.open()
                self.new_game()


        #Check for snake colliding with wall
        if not self.collides_widget(self, head):
            c=Label(text="Game Over")
            popup=Popup(title='Snake Mania',content=c,size_hint=(None, None),size=(400,400),auto_dismiss=True)
            popup.open()
            self.new_game()




class MainApp(App):
    def on_start(self):
        self.root.new_game()
        Clock.schedule_interval(self.root.next_frame, .25)
    pass


MainApp().run()
