from tkinter import * 
from PIL import Image, ImageTk
import random

MOVE_INCREMENT = 20
MOVE_PER_SECOND = 1
GAME_SPEED = 100 // MOVE_PER_SECOND
class Snake(Canvas):
    def __init__(self):
        super().__init__(width=600,
                        height=620,
                        background='black',
                        highlightthickness=0)
        #ตำแหน่งของงูและผลไม้            
        self.reset = [(100,100),(80,100),(60,100)]
        self.snake_positions = [(100,100),(80,100),(60,100)]
        self.food_positions = (200,200)
        self.score = 0
        #ดึงค่า key
        self.bind_all('<Key>',self.on_key_press)
        self.bind('<F1>', self.rungame)
        self.direction = 'Right'

        self.load_asstes()
        self.create_objects()
        
        self.rungame()
        self.starting = True
        

    def load_asstes(self):
        #กำหนดรูปงู 
        self.snake_body_image = Image.open('./desktop/body.png')
        self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
        #กำหนดรูปผลไม้
        self.food_image = Image.open('./desktop/food.png')
        self.food = ImageTk.PhotoImage(self.food_image)

    def create_objects(self):
        #กำหนดตำแหน่ง Score
        FONT = (None,15)
        self.create_text(45,12,text='Score: {}'.format(self.score),tag='score',fill='red',font=FONT)


        for x_pos , y_pos in self.snake_positions:
            self.create_image(x_pos,y_pos,image=self.snake_body,tag='snake')
        self.create_image(self.food_positions[0],self.food_positions[1],image=self.food,tag='food')
        self.create_rectangle(7,27,593,613,outline='#FFF')

    def move_snake(self):
        #ความยาวงู
        head_x,head_y = self.snake_positions[0]
        #กำหนดทิศทางกับปุ่ม
        if self.direction == 'Right':
            new_head_pos = (head_x + MOVE_INCREMENT, head_y)
        elif self.direction == 'Left':
            new_head_pos = (head_x - MOVE_INCREMENT, head_y)
        elif self.direction == 'Up':
            new_head_pos = (head_x , head_y - MOVE_INCREMENT)
        elif self.direction == 'Down':
            new_head_pos = (head_x , head_y + MOVE_INCREMENT)

        
        self.snake_positions = [new_head_pos] + self.snake_positions[:-1]

        findsnake = self.find_withtag('snake')
        for segment, pos in zip(findsnake,self.snake_positions):
            self.coords(segment,pos)

    def rungame(self):
        if self.check_collisions() and self.starting == True:
            self.after_cancel(self.loop)
            self.starting = False
            self.delete('all')
            self.create_text(300,300,justify=CENTER,
                                        text=f'GAME OVER\n\nScore: {self.score}\n\nNew Game <F1>',
                                        fill='red',font=(None,30))

        elif self.check_collisions() and self.starting == False:
			
            self.delete('all')
            self.snake_positions = self.reset
            self.food_positions = self.set_new_food_position()
            self.create_objects()
            self.starting = True
            self.direction = 'Right'
            self.score = 0
            self.loop = self.after(GAME_SPEED,self.rungame)
        else:
			
            self.check_food_collisions()
            self.move_snake()
            #กำหนด speed และสั่งให้เกม loop
            self.loop = self.after(GAME_SPEED,self.rungame)     

    def on_key_press(self,e):
        #กำหนด key
        new_direction = e.keysym # key pressed

        all_direction = ('Up','Down','Left','Right')
        opposites = ({'Up','Down'},{'Left','Right'})

        if (new_direction in all_direction and {new_direction,self.direction} not in opposites  ):
            self.direction = new_direction
        elif new_direction == 'F1':
            self.rungame()
        print('KEY:',self.direction)

    def check_collisions(self):
        #กำหนดไม่ให้เกินขอบ
        head_x, head_y = self.snake_positions[0]
        return (head_x in (0,600) or head_y in (20,620) or (head_x,head_y) in self.snake_positions[1:])

    def check_food_collisions(self):
        #เช็คถ้ากิน food ให้เพิ่มความยาวและกำหนดค่าผลไม่ใหม่
        if self.snake_positions[0] == self.food_positions:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1],image=self.snake_body,tag='snake')
            score = self.find_withtag('score')
            self.itemconfigure(score,text='Score: {}'.format(self.score),tag='score')
            self.food_positions = self.set_new_food_position()
            self.coords(self.find_withtag('food'),self.food_positions) 


    def set_new_food_position(self):
        #สุ่มตำแหน่ง foood
        while True:
            x_pos = random.randint(1,29) * MOVE_INCREMENT
            y_pos = random.randint(3,30) * MOVE_INCREMENT
            food_positions = (x_pos,y_pos)
            if food_positions not in self.snake_positions:
                    return food_positions



GUI = Tk()
GUI.title('Snake Game by Twenytwo')
GUI.resizable(False,False)

game = Snake()
game.pack()

GUI.mainloop()