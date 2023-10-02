import turtle  #turtle is a library which helps to make shapes/design using turtle object
from time import time   #time is a library used to pause or delay the execution of our code.
from random import randint  #random is library contains randint/randrange/random
from tkinter import * #tkinter is a library used to build GUI in python
from PIL import Image,ImageTk #Python Imaging Library - 2 functions built in
import mysql.connector  #msql is RDBMS,for connectivity with py and sql
import pygame
score=0
W='' #since our W is global , ao to assign some value to it....


def snake2():
     pygame.mixer.init() #initializes the audio mixer in Pygame
     sound = pygame.mixer.Sound("s1.mp3")
     sound.play()
     import turtle 
     import random
     import time
     delay=0.1 #produce gap in between the snake movement
     score=0

     #snakebodies
     bodies=[] #array to store body of snake
     position=[(0,0),(600,600),(-100,200),(0,180),(-250,250),(-220,0),(-290,290)] #array of positions
     
     #Getting a screen canvas
     W.destroy()
     s=turtle.Screen() #get screen
     s.title("Snake Game")
     s.bgcolor("white")
     s.setup(width=position[1][0],height=position[1][1])
     s.bgpic("hell.gif")
     
     
     
     #Create snake head
     head=turtle.Turtle() #turtle.Turtle() function to create a turtle object 
     head.speed(0)        #the turtle object head is being set to the fastest speed of 0(no delay)(random and smooth)
                          #10 is slowest
     head.shape("square")
     head.color("white")
     head.fillcolor("#8B1C62")
     head.penup()         #movement by the turtle will not leave a trace on the screen
     head.goto(position[0]) #goto takes 1 argument atleast
     head.direction="stop" #not move


     #snake food
     food=turtle.Turtle()
     food.speed(0)
     food.shape("square")
     food.color("yellow")
     food.fillcolor("red")
     food.penup()
     food.ht()   #hide turtle
     food.goto(position[3])
     food.st()   #show turtle


     #score board
     sb=turtle.Turtle()
     sb.shape("square")
     sb.fillcolor("black")
     sb.penup()
     sb.ht()#to hide the turtle at that posn
     sb.goto(position[2])
     sb.color("#DC143C")
     sb.write("Score : 0 ",font=("Courier",30,"bold"))

     
     def moveup():
          if head.direction!="down": #only move up when its not down(else reverse movement is there)
               head.direction="up"

     def movedown():
          if head.direction!="up":
               head.direction="down"

     def moveleft():
          if head.direction!="right":
               head.direction="left"

     def moveright():
          if head.direction!="left":
               head.direction="right"

     def movestop():
          head.direction="stop"  #game over on space key

     def move():
          if head.direction=="up":
               y=head.ycor()
               head.sety(y+20) #basically taking prev y coordinate
                               #if going up then move its movement by 20 units. 
          if head.direction=="down":
               y=head.ycor()
               head.sety(y-20)
          if head.direction=="left":
               x=head.xcor()
               head.setx(x-20)
          if head.direction=="right":
               x=head.xcor()
               head.setx(x+20)
          
          
     #Handling - key mappings

     s.listen() #the program can listen for and respond to keyboard events.
     s.onkey(moveup,"Up")
     s.onkey(movedown,"Down")
     s.onkey(moveleft,"Left")
     s.onkey(moveright,"Right")
     s.onkey(movestop,"space")   

     while True:
          s.update() #update the turtle graphics window,any changes made displayed immediately.
          
          #collision with border
          
          if head.xcor()>290:
               head.setx(-290)
          if head.xcor()<-290:
               head.setx(290)
          if head.ycor()>290:
               head.sety(-290)
          if head.ycor()<-290:
               head.sety(290)
               
          #collision with food
          if head.distance(food)<25:
               #random generation
               sound1 = pygame.mixer.Sound("eat.mp3")
               sound1.play()
               x=random.randint(-250,250)
               y=random.randint(-250,250)
               food.goto(x,y)

               #increases the length of the snake
               body=turtle.Turtle()
               body.speed(0)
               body.penup()
               body.shape("square")
               body.color("red")
               body.fillcolor("black")
               bodies.append(body) 

               #increases the score
               score+=10
               
               sb.clear() #means score 0 to change i.e. +10
               sb.color("#DC143C")
               sb.write(f"Score: {score}",font=("Courier",30,"bold"))#f string basically telling that {}is variable not a string

          #move the snake bodies it is the implementation of "stack"
          #basically head stored then others add at back
          #and take last and move and head at last to direction
          for index in range(len(bodies)-1,0,-1): #if 3 objects then head is 0 and else is 1&2 .                    
               x=bodies[index-1].xcor()           #take aage wala part before head and coordin. and goto next part
               y=bodies[index-1].ycor()
               bodies[index].goto(x,y)
          if len(bodies)>0:                       #for head ke peeche to move onto head
               x=head.xcor()
               y=head.ycor()
               bodies[0].goto(x,y)
          move()
           
          #collision with snake body
          for body in bodies:
               if body.distance(head)<20:#each part if distance from body is less than 20
                    sound.stop()
                    head.direction="stop"
               
                    #hide bodies
                    for body in bodies:
                         body.ht()
                    bodies.clear()
                    head.ht()
                    food.ht()
                    x = turtle.Turtle()
                    x.hideturtle()
                    x.penup()
                    x.goto(position[5])
                    x.color("#FF6103")
                    sound2 = pygame.mixer.Sound("gameover.wav")
                    sound2.play()
                    x.write("  G A M E   O V E R  ",font=("Tahoma",35,"bold"))
                    
                    #update score board
                    sb.clear()
                    con= mysql.connector.connect(
                    user="root",password="tiger",database="snake")
                    cur= con.cursor()
                    query="INSERT INTO score VALUES ({})".format(score)
                    cur.execute(query)
                    cur.execute("commit") #commit to reach successfully
                    con.close()
                    sb.color("#DC143C")
                    sb.write("Score: {}".format(score),font=("Courier",30,"bold"))
                    time.sleep(2)#screen delay for 2s
                    pygame.mixer.stop()
                    s.bye()
                    GUI()
                            
          time.sleep(delay)
          #pauses the execution for sometime so that the game does not run too fast for the player to follow.
     s.mainloop() #to start turtle module
     
     

def viewhigh():
     con= mysql.connector.connect(
     user="root",password="tiger",database="snake")
     cur= con.cursor() #con is to connect py and mysql
                       #cue is to execute query to respond ,cursor do all the things
     W=Tk()       
     W.geometry("200x150")
     W.configure(bg="light blue")
     W.title("HIGH SCORE")
     cur.execute("SELECT max(Score) from score")
     max_score = cur.fetchone()[0] #fetch one record in tuples
     label = Label(W,text="Highest score: {}".format(max_score), font=("Arial", 16), fg="black")
     #its a lable widget to write on window and label use padx , pady (not place method for coodinates)
     label.pack(pady=50)#creates 50pixels (dist) below so in middle it will show
     W.mainloop()

def instruct():
     W=Tk()
     W.geometry("550x450")
     W.configure(bg="orange")
     W.title("READ INSTRUCTIONS")
     L1=Label(W,text=" GAME  INSTRUCTIONS",bg="yellow",font=("TIMES NEW ROMAN",27,"bold"))
     L1.pack(fill=BOTH,padx=0,pady=0)

     L2=Label(W,text=" HOW  TO  PLAY ? ",bg="yellow",font=("TIMES NEW ROMAN",27,"bold"))
     L2.place(x=0,y=50)
     L2.pack(fill=BOTH)
     
     L3=Label(W,text=" 1) Use the arrow keys to navigate. ",bg="green",font=("TIMES NEW ROMAN",17,"bold"))
     L3.pack(fill=BOTH)
     L3.place(x=0,y=120)
     
     L4=Label(W,text=" 2) Eat the fruits to increase your score. ",bg="green",font=("TIMES NEW ROMAN",17,"bold"))
     L4.pack(fill=BOTH)
     L4.place(x=0,y=180)
     
     L5=Label(W,text=" 3) The snake can go through the boundaries. ",bg="green",font=("TIMES NEW ROMAN",17,"bold"))
     L5.pack(fill=BOTH)
     L5.place(x=0,y=240)

     L6=Label(W,text=" 4) If the head of the snake touches its body, you lose. ",bg="green",font=("TIMES NEW ROMAN",17,"bold"))
     L6.pack(fill=BOTH)
     L6.place(x=0,y=300)

     L7=Label(W,text=" 5) Use the space bar to quit. ",bg="green",font=("TIMES NEW ROMAN",17,"bold"))
     L7.pack(fill=BOTH)
     L7.place(x=0,y=360)
     
     
     
def GUI():
     global W
     W=Tk() #creates a window stored in W
     W.geometry("840x540")
     W.configure(bg="#9A32CD")
     W.title("WELCOME TO SNAKE GAME WINDOW")
     image=Image.open("ss.jpeg") #open func to take image 
     R=image.resize((300,400))     #crop and it is pixels
     R1=ImageTk.PhotoImage(R)      #type of image that can be displayed in a Tkinter window.
     Lb=Label(W,image=R1)          #box where image is to be displayed on window
     Lb.place(x=80,y=100)
     L1=Label(W,text=" PYTHON  PLAYGROUND ",bg="yellow",font=("TIMES NEW ROMAN",47,"bold"))
     L1.pack(fill=BOTH,padx=0,pady=0) #label so pad , and to start and end filled completely.fill both means take both xy

     F=Frame(height=400,bg="#E066FF",width=350)
     F.place(x=440,y=100)

     B1=Button(F,text="P L A Y",relief=SUNKEN,bg="#E0FFFF",command=snake2,fg="black",font=("Arial",20,"bold")).place(x=115,y=30)
     B2=Button(F,text="Q U I T",relief=GROOVE,bg="#E0FFFF",fg="black",command=W.destroy,font=("Arial",20,"bold")).place(x=115,y=310)
     B3=Button(F,text="H I G H S C O R E",command=viewhigh,relief=GROOVE,bg="#E0FFFF",fg="black",font=("Arial",20,"bold")).place(x=50,y=120)
     B4=Button(F,text="I N S T R U T I O N S",command=instruct,relief=GROOVE,bg="#E0FFFF",fg="black",font=("Arial",20,"bold")).place(x=25,y=215)
     W.mainloop() #interactions in a timely and efficient manner.
     #relief is txt on button how to display - raised , flat,etc.

GUI()

     


