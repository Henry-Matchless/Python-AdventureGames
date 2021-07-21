from Thing import Thing
from Room import Room
from TextUI import TextUI
#添加部分
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial
import time, os

"""
    You are a person with the ability to travel through time and space, and you live in a peaceful and warm world. 
    However, on an ordinary day, Dr. Evil broke this peace ……
    
    Dr. Evil, who lives in the future, is ready to come to the world you live in and planning to destroy your world. 
    The only way to save your world is to bring back Dr. Evil's weapons, handbooks for invasion, 
    or other important items from the future in Dr. Evil’s territory, 
    and defeat Dr. Evil through the Homeland Defense Bureau's research. 
    As the only time traveler in the current world, you have to take your time shuttle to the future Dr. Evil's home, 
    find these useful items successfully and return to your world in the time shuttle timely. 
    Of course, you can also destroy Dr. Evil by using laser weapons. But the risk is also great. 
    Once you meet Dr. Evil and without laser weapon in your hand, you will be brutally killed by him.

    According to the manual, your initial point will be the location: <OUTSIDE> of Dr. Evil's house and
    you can find your time shuttle in the location: <GARAGE>.
    You need to collect no less than 6 items(don’t exceed the limit of the backpack capacity)! 
    You need to go across many kinds of rooms to find these useful items, and even some of rooms are locked differently. 
    So what you should do is to find the keys and follow the clues to unlock the corresponding doors 
    Be careful not to be caught by Dr. Evil！Dr. Evil will catch and kill you if you go to his location: <BEDROOM>!
    The game will provide 5 different endings and evaluate the level you get –- from S to D！
"""
class Game:

    def __init__(self):
        """
        Initialises the game
        """
        self.createRooms()
        self.currentRoom = self.outside
        self.textUI = TextUI()
        self.package = []
        #初始化界面
        self.root = tk.Tk()     #TK主程序
        self.root.title("Game")     #左上角标题
        screen_width = self.root.winfo_screenwidth()    #windows屏幕宽
        screen_height = self.root.winfo_screenheight()  #windows屏幕高
        self.width = 960         #窗口宽
        self.height = 720        #窗口高
        x = (screen_width/2) - (self.width/2)        #计算中心点位置
        y = (screen_height/2) - (self.height/2)
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))   #重置窗口大小和位置
        self.root.resizable(0, 0)       #设置窗口大小不可变化
        self.root.config(bg='black')    #背景色
        #初始化游戏界面
        self.start_flag = False
        self.createGUI()
        
    #初始化游戏界面
    def createGUI(self):
        """
            Initialize the game interface
        :return:
        """
        #初始化界面
        self.imglist = {}       #保存图片对象用的
        self.player_location = [450, 210]   #玩家位置
        self.move_flag = False       #设置开始动画的标识
        #房间背景
        self.roombg = tk.Label(self.root, bd=0, width=960, height=540)  #房间背景的标签对象
        self.roombg.place(x=0, y=0, width=960, height=540)      #布置到界面上
        #绑定鼠标点击事件
        self.roombg.bind("<Button-1>", self.click)
        try:
            img = ImageTk.PhotoImage(Image.open('res/bg.png').resize((960, 540), Image.ANTIALIAS))   #缩放图片
            self.imglist['roombg'] = img    #添加图片对象到列表
            self.roombg.config(image=img)   #给标签对象加上图片背景
        except:
            print("Error: from createGUI")
        #房间名，左下角的标签
        self.roomname = tk.Label(self.root, bd=0, font=('Arial', 16), width=len('Hello')*15, bg='black', fg='white', height=20)  #房间名的标签对象
        self.roomname.place(x=0, y=520, width=len('Hello')*15, height=20)      #布置到界面上
        self.roomname.config(text='Hello')
        #文本内容框
        text_frame = tk.Frame(self.root)       #建一个容器来放
        text_frame.place(x=0, y=540, width=700, height=180)     #布置位置
        sb = tk.Scrollbar(text_frame)      #新建滚动条,这里注意下,滚动条用的是WINDOWS的风格,无法自定义
        sb.pack(side=tk.RIGHT, fill=tk.Y)     #布置位置
        self.textbox = tk.Text(text_frame, width=700, font=('Arial', 12), bg='black', fg='white',
                               yscrollcommand=sb.set, wrap='char', state=tk.DISABLED)    #新建文本框
        self.textbox.pack(expand=tk.YES, fill=tk.BOTH)       #布置文本框
        sb.config(command=self.textbox.yview)      #关联滚动条功能
        self.textbox.config(state=tk.DISABLED)   #禁止文本框修改
        #操作按钮
        #help        
        self.help_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID, command=partial(self.processCommand, ("help", None)))       #创建按钮对象
        self.help_button.place(x=740, y=580, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/help.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['help'] = img    #添加图片对象到列表
            self.help_button.config(image=img, state=tk.DISABLED)       #关联按钮图案,先设置为不可用
        except:
            print("Error: from createGUI button")
        #map
        self.map_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID, command=partial(self.processCommand, ("map", None)))       #创建按钮对象
        self.map_button.place(x=820, y=580, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/map.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['map'] = img    #添加图片对象到列表
            self.map_button.config(image=img, state=tk.DISABLED)       #关联按钮图案,先设置为不可用
        except:
            print("Error: from createGUI button")
        #check
        self.check_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID, command=partial(self.processCommand, ("check", None)))       #创建按钮对象
        self.check_button.place(x=900, y=580, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/check.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['check'] = img    #添加图片对象到列表
            self.check_button.config(image=img, state=tk.DISABLED)       #关联按钮图案,先设置为不可用
        except:
            print("Error: from createGUI button")
        #pickup
        self.pickup_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID, command=partial(self.processCommand, ("pickup", None)))       #创建按钮对象
        self.pickup_button.place(x=740, y=640, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/pickup.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['pickup'] = img    #添加图片对象到列表
            self.pickup_button.config(image=img, state=tk.DISABLED)       #关联按钮图案,先设置为不可用
        except:
            print("Error: from createGUI button")
        #inventory
        self.inventory_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID, command=partial(self.processCommand, ("inventory", None)))       #创建按钮对象
        self.inventory_button.place(x=820, y=640, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/inventory.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['inventory'] = img    #添加图片对象到列表
            self.inventory_button.config(image=img, state=tk.DISABLED)       #关联按钮图案,先设置为不可用
        except:
            print("Error: from createGUI button")
        #quit
        self.quit_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID, command=partial(self.processCommand, ("quit", None)))       #创建按钮对象
        self.quit_button.place(x=900, y=640, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/quit.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['quit'] = img    #添加图片对象到列表
            self.quit_button.config(image=img, state=tk.DISABLED)       #关联按钮图案,先设置为不可用
        except:
            print("Error: from createGUI button")
        #四个门
        #south
        self.south_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID)       #创建按钮对象
        self.south_button.place(x=460, y=490, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/south.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['south'] = img    #添加图片对象到列表
            self.south_button.config(image=img)       #关联按钮图案
        except:
            print("Error: from createGUI button")
        self.south_button.place(x=460, y=490, width=0, height=0)       #隐藏按钮位置
        #north
        self.north_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID)       #创建按钮对象
        self.north_button.place(x=460, y=10, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/north.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['north'] = img    #添加图片对象到列表
            self.north_button.config(image=img)       #关联按钮图案
        except:
            print("Error: from createGUI button")
        self.north_button.place(x=460, y=10, width=0, height=0)       #隐藏按钮位置
        #east
        self.east_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID)       #创建按钮对象
        self.east_button.place(x=910, y=250, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/east.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['east'] = img    #添加图片对象到列表
            self.east_button.config(image=img)       #关联按钮图案
        except:
            print("Error: from createGUI button")
        self.east_button.place(x=910, y=250, width=0, height=0)       #隐藏按钮位置
        #west
        self.west_button = tk.Button(self.root, bd=0, bg='black', activebackground='black',
                                     width=40, height=40, relief=tk.SOLID)       #创建按钮对象
        self.west_button.place(x=10, y=250, width=40, height=40)       #布置按钮位置
        try:
            img = ImageTk.PhotoImage(Image.open('res/west.png').resize((40, 40), Image.ANTIALIAS))   #缩放图片
            self.imglist['west'] = img    #添加图片对象到列表
            self.west_button.config(image=img)       #关联按钮图案
        except:
            print("Error: from createGUI button")
        self.west_button.place(x=10, y=250, width=0, height=0)       #隐藏按钮位置        
        #物品对象
        self.thing = tk.Button(self.root, bd=0, width=50, height=50, relief=tk.SOLID)  #物品对象
        self.thing.place(x=720, y=150, width=50, height=50)      #布置到界面上(右上方)
        #怪物对象
        self.monster_flag = True
        self.monster = tk.Button(self.root, bd=0, width=60, height=80, command=partial(self.move, [450, 210], ("attack", None)))  #怪物对象
        self.monster.place(x=450, y=210, width=100, height=100)      #布置到界面上(右上方)
        try:
            img = ImageTk.PhotoImage(Image.open('res/monster.png').resize((100, 100), Image.ANTIALIAS))   #缩放图片
            self.imglist['monster'] = img    #添加图片对象到列表
            self.monster.config(image=img)   #给标签对象加上图片背景
        except:
            print("Error: from createGUI object")
        #人物对象
        self.player = tk.Label(self.root, bd=0, width=48, height=64)  #人物对象
        self.player.place(x=450, y=210, width=48, height=64)      #布置到界面上(正中)
        try:
            img = ImageTk.PhotoImage(Image.open('res/player.png').resize((48, 64), Image.ANTIALIAS))   #缩放图片
            self.imglist['player'] = img    #添加图片对象到列表
            self.player.config(image=img)   #给标签对象加上图片背景
        except:
            print("Error: from createGUI object")
        #小地图对象,放到最下面可以在最上层
        self.minimap_flag = True
        self.minimap = tk.Label(self.root, bd=0, width=960, height=340)  #小地图对象
        self.minimap.place(x=0, y=100, width=960, height=340)      #布置到界面上
        try:
            img = ImageTk.PhotoImage(Image.open('res/minimap.png').resize((500, 350), Image.ANTIALIAS))   #缩放图片
            self.imglist['minimap'] = img    #添加图片对象到列表
            self.minimap.config(image=img)   #给标签对象加上图片背景
        except:
            print("Error: from createGUI object")
        #背包对象
        from Package import PackageGUI
        self.package_flag = True
        self.packagegui = PackageGUI(self.root)     #背包对象
        self.packagegui.place(x=300, y=60, width=360, height=400)   #布置到界面上
        #开始按钮  
        self.start_button = tk.Button(self.root, text='Start Game', font=('Arial', 16),
                                      bd=0, width=180, height=40, relief=tk.SOLID, command=self.start)       #创建按钮对象
        self.start_button.place(x=390, y=280, width=180, height=40)       #布置按钮位置

    #刷新当前房间
    def updateRoom(self):
        """
            Refresh the current room
        :return:
        """
        #隐藏开始按钮
        self.start_button.place(x=390, y=280, width=0, height=0)       #隐藏按钮位置
        #如果存在当前房间
        if self.currentRoom:
            roomname = self.currentRoom.roomname    #提取房间名
            #缩小小地图
            self.minimap_flag = False
            self.minimap.place(x=0, y=100, width=0, height=0)      #隐藏小地图
            #设置房间的背景(不同房间可以不同背景)
            try:
                imgpath = 'res/room_'+roomname+'.png'
                if os.path.exists(imgpath):
                    img = ImageTk.PhotoImage(Image.open(imgpath).resize((960, 540), Image.ANTIALIAS))   #缩放图片
                    self.imglist['room_'+roomname] = img    #添加图片对象到列表
                    self.roombg.config(image=img)   #给标签对象加上图片背景
                else:
                    self.roombg.config(image=self.imglist['roombg'])   #给标签对象加上图片背景
            except Exception as e:
##                print(str(e))
                pass
            #设置门
            exits = self.currentRoom.exits  #提取可以走的方向
            if "upstairs" in exits or "north" in exits:
                self.north_button.place(x=460, y=10, width=40, height=40)       #布置按钮位置
                #设置按钮功能
                if "upstairs" in exits:
                    command = ('go', 'upstairs')
                    self.north_button.config(command=partial(self.move, [456, 50], command))
                else:
                    command = ('go', 'north')
                    self.north_button.config(command=partial(self.move, [456, 50], command))
            else:
                self.north_button.place(x=460, y=10, width=0, height=0)       #隐藏按钮位置
            if "downstairs" in exits or "south" in exits:
                self.south_button.place(x=460, y=490, width=40, height=40)       #布置按钮位置
                #设置按钮功能
                if "downstairs" in exits:
                    command = ('go', 'downstairs')
                    self.south_button.config(command=partial(self.move, [456, 426], command))
                else:
                    command = ('go', 'south')
                    self.south_button.config(command=partial(self.move, [456, 426], command))
            else:
                self.south_button.place(x=460, y=490, width=0, height=0)       #隐藏按钮位置
            if "east" in exits:
                self.east_button.place(x=910, y=250, width=40, height=40)       #布置按钮位置
                command = ('go', 'east')
                self.east_button.config(command=partial(self.move, [862, 238], command))
            else:
                self.east_button.place(x=910, y=250, width=0, height=0)       #隐藏按钮位置
            if "west" in exits:
                self.west_button.place(x=10, y=250, width=40, height=40)       #布置按钮位置
                command = ('go', 'west')
                self.west_button.config(command=partial(self.move, [50, 238], command))
            else:
                self.west_button.place(x=10, y=250, width=0, height=0)       #隐藏按钮位置
            #修改房间标签            
            self.roomname.config(text=roomname, width=len(roomname)*15)
            self.roomname.place(x=0, y=520, width=len(roomname)*15, height=20)      #布置到界面上
            #确认物品
            if self.currentRoom.things:
                temp = self.currentRoom.things[0]
                #设置物品的图片
                try:
                    imgpath = 'res/bthing'+str(temp.type)+'.png'
                    if os.path.exists(imgpath):
                        img = ImageTk.PhotoImage(Image.open(imgpath).resize((50, 50), Image.ANTIALIAS))   #缩放图片
                    else:
                        img = ImageTk.PhotoImage(Image.open('res/bthing.png').resize((50, 50), Image.ANTIALIAS))   #缩放图片
                    self.imglist['bthing'+str(temp.type)] = img    #添加图片对象到列表
                    self.thing.config(image=img)    #给按钮加上图片
                except Exception as e:
##                    print(str(e))
                    print("Error: from updateRoom item pics")
                #设置物品位置,同时修改pickup功能
                self.thing.config(command=partial(self.move, temp.location, ("pickup", temp.location)))
                self.pickup_button.config(command=partial(self.move, temp.location, ("pickup", temp.location)))
                self.thing.place(x=temp.location[0], y=temp.location[1], width=50, height=50)      #布置到界面上
            else:
                self.thing.place(x=720, y=150, width=0, height=0)      #隐藏物品按钮
                self.pickup_button.config(command=partial(self.processCommand, ("pickup", None)))   #恢复pickup功能不用移动人物
            #确认怪物
            if self.currentRoom == self.bedroom and self.monster_flag:                        
                self.monster.place(x=450, y=210, width=100, height=100)     #显示怪物   
            else:
                self.monster.place(x=450, y=210, width=0, height=0)     #隐藏怪物   

    #添加内容到文本框
    def addMsg(self, msg):
        """
            add message
        :return:
        """
        self.textbox.config(state=tk.NORMAL)   #开放文本框修改权限
        self.textbox.insert('end', msg)     #在文本框最底部加上内容
        self.textbox.config(state=tk.DISABLED)   #禁止文本框修改
        self.textbox.see(tk.END)    #自动滚动到最底部

    #开始游戏
    def start(self):
        """
        Initialises the game
        """
        self.createRooms()
        self.currentRoom = self.outside
        self.textUI = TextUI()
        self.package = []
        self.start_flag = True
        #欢迎词
        self.printWelcome()
        #缩小小地图
        self.minimap_flag = False
        self.minimap.place(x=0, y=100, width=0, height=0)      #隐藏小地图
        #缩小背包
        self.package_flag = False
        self.packagegui.place(x=300, y=60, width=0, height=0)   #隐藏背包
        #刷新房间
        self.updateRoom()
        #设置按钮可用
        self.help_button.config(state=tk.NORMAL)
        self.map_button.config(state=tk.NORMAL)
        self.check_button.config(state=tk.NORMAL)
        self.pickup_button.config(state=tk.NORMAL)
        self.inventory_button.config(state=tk.NORMAL)
        self.quit_button.config(state=tk.NORMAL)
        #显示人物在最中央
        self.player.place(x=450, y=210, width=48, height=64)      #布置到界面上(正中)

    #开始界面
    def startPage(self):
        """
            start interface
        :return:
        """
        #缩小小地图
        self.minimap_flag = False
        self.minimap.place(x=0, y=100, width=0, height=0)      #隐藏小地图
        #缩小背包
        self.package_flag = False
        self.packagegui.place(x=300, y=60, width=0, height=0)   #隐藏背包
        #怪物存在
        self.monster_flag = True
        self.monster.place(x=720, y=150, width=0, height=0)      #隐藏怪物
        #关闭门
        self.north_button.place(x=460, y=10, width=0, height=0)       #隐藏按钮位置
        self.south_button.place(x=460, y=490, width=0, height=0)       #隐藏按钮位置
        self.east_button.place(x=910, y=250, width=0, height=0)       #隐藏按钮位置
        self.west_button.place(x=10, y=250, width=0, height=0)       #隐藏按钮位置
        #修改房间标签
        roomname = 'Hello'
        self.roomname.config(text=roomname, width=len(roomname)*15)
        self.roomname.place(x=0, y=520, width=len(roomname)*15, height=20)      #布置到界面上
        #设置按钮不可用
        self.help_button.config(state=tk.DISABLED)
        self.map_button.config(state=tk.DISABLED)
        self.check_button.config(state=tk.DISABLED)
        self.pickup_button.config(state=tk.DISABLED)
        self.inventory_button.config(state=tk.DISABLED)
        self.quit_button.config(state=tk.DISABLED)
        #隐藏人物
        self.player.place(x=450, y=210, width=0, height=0)      #隐藏人物
        #隐藏物品按钮
        self.thing.place(x=720, y=150, width=0, height=0)      #隐藏物品按钮
        #隐藏怪物
        self.monster.place(x=450, y=210, width=0, height=0)      #隐藏怪物

    #玩家移动效果
    def move(self, location, command):
        """
            Player movement effects
        :return:
        """
        if not self.move_flag:
##            print(self.player_location, location , command)
##            print(self.package)
            self.move_flag = True       #设置开始动画的标识
            ox = self.player_location[0]
            oy = self.player_location[1]
            nx = location[0]
            ny = location[1]                    
            #更新动画用到的属性
            self.location = location    #动画的目标位置            
            self.command = command      #动画完成后执行的动作
            framenum = 45       #设置45帧完成动画效果
            speed = (840-60)/framenum  #行走速度
            sframe = (abs(ox-nx)**2+abs(oy-ny)**2)**0.5 / speed
            if sframe:
                self.mx = (ox-nx)/sframe  #X轴一帧走的偏移量
                self.my = (oy-ny)/sframe  #Y轴一帧走的偏移量
            else:
                self.mx = 0
                self.my = 0
##            print(sframe, speed, self.mx, self.my)        
            self.moving()

    #移动动画实现
    def moving(self):
        """
            Implementation of Animation
        :return:
        """
        if self.move_flag:
            self.player_location[0] -= self.mx
            self.player_location[1] -= self.my
            if self.player_location[0]<=self.location[0]+abs(self.mx)+0.1 and self.player_location[1]<=self.location[1]+abs(self.my)+0.1 \
               and self.player_location[0]>=self.location[0]-abs(self.mx)-0.1 and self.player_location[1]>=self.location[1]-abs(self.my)-0.1:   #到达目标位置
                self.move_flag = False
                if self.command:        #如果有操作
                    self.processCommand(self.command)       #操作                
                    return
            #更新人物位置
            self.player.place(x=self.player_location[0], y=self.player_location[1], width=48, height=64)
            #执行动画效果
            self.root.after(33, self.moving)    #33ms一帧,1s 30帧

    def createRooms(self):
        """
            Sets up all room assets
        :return: None
        """
        #这里初始化要把房间名称也加上
        self.outside = Room("Outside", "You are outside")
        
        self.lobby = Room("Lobby", "in the lobby")
        self.lobby.createThing("laser weapons", 0, 66)

        self.policeoffice = Room("Police Office", "You are in the police office")
        self.policeoffice.createThing("key 4 --- clue: can open a room near the police office",4,1)

        self.prison = Room("Prison", "You are in the prison")
        self.prison.setLock(4)
        self.prison.createThing("The hair of a mutant",14)

        self.plants = Room("Manufacturing Plants", "in a manufacturing plants")

        self.lab = Room("Future Factory Laboratory", "in the future factory Laboratory")
        self.lab.createThing("key 3 --- clue: can open a room near the Dr. Evil's office", 3, 1)

        self.office = Room("Dr. Evil's Office", "in the Dr. Evil's office")
        self.office.createThing("key 2 --- clue: can open a room near the future factory Laboratory", 2, 1)

        self.archive = Room("Scientific And Technical Archives Room", "in the  scientific and technical archives room") #locked has thing
        self.archive.setLock(1)
        self.archive.createThing("confidential manufacturing files", 10, 2)

        self.storeroom = Room("Hi-tech Products Storeroom", "in the hi-tech products storeroom") # locked has thing
        self.storeroom.setLock(2)
        self.storeroom.createThing("time machine", 11, 2)

        self.conference = Room("Conference Room", "in the conference room")
        self.conference.createThing("Dr. Evil's notebook for invading", 15, 2)

        self.restaurant = Room("Restaurant", "in the restaurant") # has food
        self.restaurant.createThing("artificial meat burger", 13)

        self.finance = Room("Vault", "in the vault") # locked
        self.finance.setLock(3)
        self.finance.createThing("key 1 --- clue: can open a room near the manufacturing plants", 1, 1)

        self.garage = Room("Garage", "in the garage, your time shuttle is in there, you can back to your world ------ quit")
        self.garage.createThing("gravity apparatus", 14)

        self.bedroom = Room("Dr. Evil's Bedroom", "in the Dr. Evil's bedroom, you woke Dr. Evil up and he caught you! Mission failed! You can quit the game and start it again!")

        self.outside.setExit("east", self.lobby)
        self.outside.setExit("south", self.lab)
        self.outside.setExit("west", self.plants)
        self.outside.setExit("north",self.policeoffice)

        self.policeoffice.setExit("upstairs",self.prison)
        self.policeoffice.setExit("south",self.outside)

        self.prison.setExit("downstairs",self.policeoffice)

        self.lobby.setExit("west", self.outside)
        self.lobby.setExit("east", self.restaurant)
        self.restaurant.setExit("west", self.lobby)

        self.plants.setExit("east", self.outside)
        self.plants.setExit("west", self.archive)
        self.plants.setExit("south", self.garage)
        self.plants.setExit("north", self.conference)
        self.archive.setExit("east", self.plants)
        self.garage.setExit("north", self.plants)
        self.conference.setExit("south", self.plants)

        self.lab.setExit("north", self.outside)
        self.lab.setExit("east", self.office)
        self.lab.setExit("west", self.storeroom)
        self.storeroom.setExit("east", self.lab)

        self.office.setExit("west", self.lab)
        self.office.setExit("east", self.finance)
        self.office.setExit("south", self.bedroom)

        self.bedroom.setExit("north", self.office)

        self.finance.setExit("west", self.office)

        self.win = False

    def play(self):
        """
            The main play loop
        :return: None
        """
        self.printWelcome()
        finished = False
        while (finished == False):
            command = self.textUI.getCommand()      # Returns a 2-tuple
            finished = self.processCommand(command)
##            print('command:', command)

        print("Thank you for playing!")
        self.addMsg("Thank you for playing!\n")

    def printWelcome(self):
        """
            Displays a welcome message
        :return:
        """
        """
        self.textUI.printtoTextUI("You are a person with the ability to travel through time and space, and you live in a peaceful and warm world. However, on an ordinary day, Dr. Evil broke this peace ……")
        self.textUI.printtoTextUI("Dr. Evil, who lives in the future, is ready to come to the world you live in and planning to destroy your world.")
        self.textUI.printtoTextUI("The only way to save your world is to bring back Dr. Evil's weapons, handbooks for invasion, or other important items from the future in Dr. Evil’s territory, and defeat Dr. Evil through the Homeland Defense Bureau's research.")
        self.textUI.printtoTextUI("As the only time traveler in the current world, you have to take your time shuttle to the future Dr. Evil's home, find these useful items successfully and return to your world in the time shuttle timely.")
        self.textUI.printtoTextUI("According to the manual, your initial point will be the location:<OUTSIDE> of Dr. Evil's house and you can find your time shuttle in the location:<GARAGE>.")
        self.textUI.printtoTextUI("You need to collect no less than 6 items! Be careful not to be caught by Dr. Evil unless you have the laser weapons! He may be waiting for you in one of these rooms! ")
        self.textUI.printtoTextUI("")
        self.textUI.printtoTextUI("")
        # self.textUI.printtoTextUI(f'Your command words are: {self.showCommandWords()}')
        """
        #添加文本
        text = "You are a person with the ability to travel through time and space, and you live in a peaceful and warm world. However, on an ordinary day, Dr. Evil broke this peace ……\n"
        text = text + "Dr. Evil, who lives in the future, is ready to come to the world you live in and planning to destroy your world.\n"
        text = text + "The only way to save your world is to bring back Dr. Evil's weapons, handbooks for invasion, or other important items from the future in Dr. Evil’s territory, and defeat Dr. Evil through the Homeland Defense Bureau's research.\n"
        text = text + "As the only time traveler in the current world, you have to take your time shuttle to the future Dr. Evil's home, find these useful items successfully and return to your world in the time shuttle timely.\n"
        text = text + "According to the manual, your initial point will be the location:<OUTSIDE> of Dr. Evil's house and you can find your time shuttle in the location:<GARAGE>.\n"
        text = text + "You need to collect no less than 6 items! Be careful not to be caught by Dr. Evil unless you have the laser weapons! He may be waiting for you in one of these rooms! \n"
        text = text + "\n"
        text = text + "\n"
        # text = text + f'Your command words are: {self.showCommandWords()}\n'
        self.addMsg(text)
        #弹窗提示
        messagebox.showinfo(title='warn', message=text)

    def showCommandWords(self):
        """
            Show a list of available commands
        :return: None
        """
        return ['help', 'map', 'go', 'check', 'pickup', 'inventory', 'quit']

    def processCommand(self, command):
        """
            Process a command from the TextUI
        :param command: a 2-tuple of the form (commandWord, secondWord)
        :return: True if the game has been quit, False otherwise
        """
        commandWord, secondWord = command
        if commandWord != None:
            commandWord = commandWord.upper()

        wantToQuit = False
        if commandWord == "HELP":
            self.doPrintHelp()
        elif commandWord == "MAP":
            self.doPrintMap()
        elif commandWord == "GO":
            self.doGoCommand(secondWord)
        elif commandWord == "CHECK":
            self.doCheckCommand()
        elif commandWord == "PICKUP":
            self.doPickUpCommand(secondWord)
        elif commandWord == "ATTACK":
            self.doAttackCommand(secondWord)
        elif commandWord == "INVENTORY":
            self.doPackageCommand()
        elif commandWord == "QUIT": # quit the game, you can quit the game anytime as you want but you may lose the game. while the game has 2 endings --- 1.come back but cannot save your world.(bad ending) 2.come back and save your world successfully.(happy ending)
            text = ""
            self.start_flag = False     #设置游戏结束
            if self.currentRoom == self.bedroom:
                """
                self.textUI.printtoTextUI("-------- You lose! Level: D --------\nSADLY: You were captured and brutally murdered by Dr. Evil!")
                """
                text = text + "-------- You lose! Level: D --------\nSADLY: You were captured and brutally murdered by Dr. Evil!"
            else:
                if self.checkIsWin() == False and self.currentRoom != self.garage:
                    """
                    self.textUI.printtoTextUI("-------- You lose! Level: C --------\nSORRY: You didn't find the garage to back to your world!")
                    """
                    text = text + "-------- You lose! Level: C --------\nSORRY: You didn't find the garage to back to your world!"
                elif self.checkIsWin() == False and self.currentRoom == self.garage:
                    """
                    self.textUI.printtoTextUI("-------- You win! Level: A --------\nWELL DONE: You took a time shuttle back to your world safely but you didn't bring back enough future supplies to make the research continue!!! You can not save your world!! What a pity!")
                    """
                    text = text + "-------- You win! Level: A --------\nWELL DONE: You took a time shuttle back to your world safely but you didn't bring back enough future supplies to make the research continue!!! You can not save your world!! What a pity!"
                elif self.checkIsWin() == True and self.currentRoom == self.garage:
                    """
                    self.textUI.printtoTextUI("-------- You win! Level: S --------\nPERFECT: You took a time shuttle back to your world safely and you've finally developed a weapon to save the world!")
                    """
                    text = text + "-------- You win! Level: S --------\nPERFECT: You took a time shuttle back to your world safely and you've finally developed a weapon to save the world!"
                elif self.checkIsWin() == True and self.currentRoom != self.garage:
                    """
                    self.textUI.printtoTextUI("-------- You lose! Level: B --------\nSORRY: Although you have found enough useful items, You didn't find the garage to back to your world!")
                    """
                    text = text + "-------- You lose! Level: B --------\nSORRY: Although you have found enough useful items, You didn't find the garage to back to your world!"
            wantToQuit = True
            self.addMsg(text)
            #弹窗提示
            messagebox.showinfo(title='warn', message=text)
            #保存日志
            self.saveGame()
            self.root.quit()
        else:
            # Unknown command ...
            self.textUI.printtoTextUI("Don't know what you mean")

        return wantToQuit

    def doPrintHelp(self): # that is the --help information of this game.
        """
            Display some useful help text
        :return: None
        """
        """
        self.textUI.printtoTextUI("You need to collect some useful items from Dr. Evil's rooms and find your time shuttle in the <GARAGE>.")
        self.textUI.printtoTextUI("Dr. Evil's rooms will have a lot of secret rooms which means you need to crack it successfully with your wisdom.")
        self.textUI.printtoTextUI("You need to collect no less than 6 items! Be careful not to be caught by Dr. Evil unless you have the laser weapons!")
        self.textUI.printtoTextUI("")
        # self.textUI.printtoTextUI(f'Your command words are: {self.showCommandWords()}')
        """
        #刷新房间
        self.updateRoom()
        #信息
        text = "You need to collect some useful items from Dr. Evil's rooms and find your time shuttle in the <GARAGE>.\n"
        text = text + "Dr. Evil's rooms will have a lot of secret rooms which means you need to crack it successfully with your wisdom.\n"
        text = text + "You need to collect no less than 6 items! Be careful not to be caught by Dr. Evil unless you have the laser weapons!\n"
        text = text + "You need to collect no less than 6 items! Be careful not to be caught by Dr. Evil unless you have the laser weapons!\n"
        text = text + "\n"
        # text = text + f'Your command words are: {self.showCommandWords()}\n'
        self.addMsg(text)
        messagebox.showinfo(title='warn', message=text)

    def doPrintMap(self):  # that is the -- print map of this game.
        """
            Display map
        :return: None
        """
        """
        print("                                                             |-------------------|                                                       ")
        print("         N                                                   |      prison       |                                                       ")
        print("     W       E                                               |-------------------|                                                       ")
        print("         S                                                            | |                                                                ")
        print("                                                                      | |                                                                ")
        print("                                    |-------------------|    |-------------------|                                                       ")
        print("                                    |  conference room  |    |   police office   |                                                       ")
        print("                                    |-------------------|    |-------------------|                                                       ")
        print("                                              | |                    | |                                                                 ")
        print("                                              | |                    | |                                                                 ")
        print("           |-------------------|    |-------------------|    |-------------------|      |-------------------|      |-------------------| ")
        print("           |   archives room   | == |      plants       | == |      outside      |  ==  |       lobby       |  ==  |     restaurant    | ")
        print("           |-------------------|    |-------------------|    |-------------------|      |-------------------|      |-------------------| ")
        print("                                              | |                    | |                                                                 ")
        print("                                    |-------------------|            | |                                                                 ")
        print("                                    |      garage       |            | |                                                                 ")
        print("                                    |-------------------|            | |                                                                 ")
        print("                                                                     | |                                                                 ")
        print("                                    |-------------------|    |-------------------|     |-------------------|     |-------------------|   ")
        print("                                    | hi-tech storeroom | == |    future  lab    |  == |   Dr.E's office   |  == |      vault        |   ")
        print("                                    |-------------------|    |-------------------|     |-------------------|     |-------------------|   ")
        print("                                                                                                | |                                      ")
        print("                                                                                       |-------------------|                             ")
        print("                                                                                       |  Dr.E's bedroom   |                             ")
        print("                                                                                       |-------------------|                             ")
        """
        #显示/关闭小地图
        if self.minimap_flag:
            self.minimap_flag = False
            self.minimap.place(x=0, y=100, width=0, height=0)      #隐藏小地图
        else:
            self.minimap_flag = True
            self.minimap.place(x=0, y=100, width=960, height=340)      #打开小地图

    def doGoCommand(self, secondWord):
        """
            Performs the GO command
        :param secondWord: the direction the player wishes to travel in
        :return: None
        """
        if secondWord == None:
            # Missing second word ...
            self.textUI.printtoTextUI("Go where? Such as you can enter <go north> to make the character walk to the north")
            return

        nextRoom = self.currentRoom.getExit(secondWord)
        if nextRoom == None:
            self.textUI.printtoTextUI(f"There has no door in the <{secondWord}> or you spelled words wrongly!")
        else:
            # Check if the room is locked here
            if nextRoom.needKey():
                """
                self.textUI.printtoTextUI(f"The room need key:{nextRoom.getLockId()}")
                """
                self.addMsg(f"The room need key:{nextRoom.getLockId()}\n")
                if self.checkHasKey(nextRoom.getLockId()):
                    """
                    self.textUI.printtoTextUI(f"I have the key:{nextRoom.getLockId()} in my package!! unlock the room.")
                    """
                    self.addMsg(f"I have the key:{nextRoom.getLockId()} in my package!! unlock the room.\n")
                    self.useKey(nextRoom.getLockId())
                    nextRoom.setLock(0)
                else:
                    """
                    self.textUI.printtoTextUI(f"I need to find the key:{nextRoom.getLockId()} in other room.")
                    """
                    self.addMsg(f"I need to find the key:{nextRoom.getLockId()} in other room.\n")
                    messagebox.showinfo(title='warn', message=f"I need to find the key:{nextRoom.getLockId()} in other room.\n")
                    return
            self.currentRoom = nextRoom            
            self.addMsg(self.currentRoom.getLongDescription()+'\n')
##                messagebox.showinfo(title='warn', message=self.currentRoom.getLongDescription()+'\n')
            #刷新显示房间
            self.updateRoom()
            #刷新人物位置
            if secondWord == 'upstairs' or secondWord == 'north':   #从上方进门,出来在最下
                self.player.place(x=456, y=426, width=48, height=64)      #布置到界面上(最下)
                self.player_location = [456, 426]
            elif secondWord == 'downstairs' or secondWord == 'south':   #从下方进门,出来在最上
                self.player.place(x=456, y=50, width=48, height=64)      #布置到界面上(最上)
                self.player_location = [456, 50]
            elif secondWord == 'west':          #从左方进门,出来在最右
                self.player.place(x=862, y=238, width=48, height=64)      #布置到界面上(最右)
                self.player_location = [862, 238]
            elif secondWord == 'east':          #从右方进门,出来在最左
                self.player.place(x=50, y=238, width=48, height=64)      #布置到界面上(最左)
                self.player_location = [50, 238]

    def doCheckCommand(self): # Check whether the place has supplies or not.
        """
            Performs the CHECK command
        :return: None
        """
        if self.currentRoom.isEmpty():
            """
            self.textUI.printtoTextUI("There's nothing here!")
            """
            self.addMsg("There's nothing here!\n")
            messagebox.showinfo(title='warn', message="There's nothing here!\n")
        else:
            """
            self.textUI.printtoTextUI(f"Find: {self.currentRoom.listThing()}!")
            self.textUI.printtoTextUI(self.currentRoom.checkThingType())
            """
            self.addMsg(f"Find: {self.currentRoom.listThing()}!\n")
            self.addMsg(self.currentRoom.checkThingType()+"\n")
            messagebox.showinfo(title='warn', message=f"Find: {self.currentRoom.listThing()}!\n"+self.currentRoom.checkThingType()+"\n")
            

    def doPickUpCommand(self, secondWord): # If the place has supplies then you can pick it up and store it in your package.
        """
            Performs the PICKUP command
        :return: None
        """
        if self.currentRoom.isEmpty():
            """
            self.textUI.printtoTextUI("There's nothing here!")
            """
            self.addMsg("There's nothing here!\n")
            messagebox.showinfo(title='warn', message="There's nothing here!\n")
        else:
            while(True):
                t = self.currentRoom.pickupThing()
                if t == None:
                    break;
                self.package.append(t)
            # self.textUI.printtoTextUI(f"Find: {self.currentRoom.listThing()}!")
            #刷新房间状态
            self.updateRoom()
            #移动人物到宝箱位置
            if secondWord:
                self.player.place(x=secondWord[0], y=secondWord[1], width=48, height=64)      #布置到物品所在位置

    #攻击怪物
    def doAttackCommand(self, secondWord):
        if len(self.package) == 0:
            """
            self.textUI.printtoTextUI(self.currentRoom.getLongDescription2())
            """
            self.addMsg(self.currentRoom.getLongDescription2()+'\n')
            messagebox.showinfo(title='warn', message=self.currentRoom.getLongDescription2()+'\n')
            self.processCommand(("quit", None))
        else:
            condition1 = 0
            for t in self.package:
                if t.type == 66:
                    condition1 += 1
            if condition1 >= 1:
                """
                self.textUI.printtoTextUI(f"You have the laser weapons and you killed Dr. Evil without hesitation！So you can come to the <garage> back to your world, Exits: ['north'] ")
                """
                self.addMsg(f"You have the laser weapons and you killed Dr. Evil without hesitation！So you can come to the <garage> back to your world, Exits: ['north'] \n")
                messagebox.showinfo(title='warn', message=f"You have the laser weapons and you killed Dr. Evil without hesitation！So you can come to the <garage> back to your world, Exits: ['north'] \n")
                #击杀成功,修改标识,刷新房间
                self.monster_flag = False
                self.updateRoom()
            else:
                """
                self.textUI.printtoTextUI(self.currentRoom.getLongDescription2())
                """
                self.addMsg(self.currentRoom.getLongDescription2()+'\n')
                messagebox.showinfo(title='warn', message=self.currentRoom.getLongDescription2()+'\n')
                self.processCommand(("quit", None))

    def doPackageCommand(self):
        """
            Performs the INVENTORY command
        :return: None
        """
        countItem = 0
        countKey = 0
        for t in self.package:
            if t.type == 1:
                countKey += 1
            elif t.type != 1:
                countItem += 1
        """
        self.textUI.printtoTextUI(f"My package has: {countItem} items and {countKey} keys, {8-countKey-countItem} left spaces")     # show all items in the package
        self.textUI.printtoTextUI(f"These are:{',   '.join([t.description for t in self.package])}")    # show all items in the package
        """
        text = f"My package has: {countItem} items and {countKey} keys, {8-countKey-countItem} left spaces\n"
        text = text + f"These are:{',   '.join([t.description for t in self.package])}\n"
        if len(self.package) >=8:  # give tips ---- Determine whether you have enough space in your backpack to store supplies. weight limits
            """
            self.textUI.printtoTextUI("Warning: Backpack capacity is not enough. No more than 8 items in your package is better!")
            """
            text = text + "Warning: Backpack capacity is not enough. No more than 8 items in your package is better!\n"
        else:
            """
            self.textUI.printtoTextUI("Your packages still have enough space.No more than 8 items in your package is better!")
            """
            text = text + "Your packages still have enough space.No more than 8 items in your package is better!\n"
        self.addMsg(text)
##        messagebox.showinfo(title='warn', message=text)
        #打开/关闭背包
        if self.package_flag:
            self.package_flag = False
            self.packagegui.place(x=0, y=100, width=0, height=0)      #隐藏背包
        else:
            self.package_flag = True
            self.packagegui.place(x=300, y=60, width=360, height=400)      #打开背包
            self.packagegui.udpate(self.package)        #更新背包内容

    def checkHasKey(self, _id):
        """
            check whether you have the right key which can open the door correctly in your package.
        :param _id: the id of the key
        :return: True if the id of the key is correct -- has key to open the door, False otherwise
        """
        for t in self.package:
            if t.type == 1 and t.id == _id:
                return True
        return False

    def useKey(self, _id):
        """
            Use the key in your backpack to open the correct door and destroy it after you finish using it.
        :param _id: the id of the key
        :return: self.package.pop(i) ---> drop the key after using and package space +1, None
        """
        for i in range(0, len(self.package)):
            t = self.package[i]
            if t.type == 1 and t.id == _id:
                return self.package.pop(i)
        return None

    def checkIsWin(self):
        """
            Check if sufficient supplies have been collected.
        :return: True if you collected enough item, False otherwise
        """
        count = 0
        for t in self.package:
            if t.type != 1:
                count += 1
                if count >= 6:  # Determine if there are enough supplies in the package (keys are not counted as supplies). You can reset one of the conditions of win (collecting how many supplies) by changing the value of number.
                    return True # if you collected more than 6 item, it will return true
        return False            # if you collected less than 6 item, it will return false

    #鼠标点击事件
    def click(self, e):
        if self.start_flag: #开始游戏后才能移动位置
            self.move([e.x, e.y], False)

    #保存LOG
    def saveGame(self):
        #日志
        text = self.textbox.get('0.0','end')
        #读取时间戳做为文件名        
        filename = str(int(time.time()))
        with open("save/" + filename +'.txt', 'w') as f:
            f.write(text)        

def main():
    game = Game()
##    game.play()
    game.createGUI()
    game.startPage()
    game.root.mainloop()

if __name__ == "__main__":
    main()

    
