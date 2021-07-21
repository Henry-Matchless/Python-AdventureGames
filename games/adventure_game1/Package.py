import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
from tkinter import messagebox
import os

#背包类
class PackageGUI(tk.Canvas):

    #初始化参数
    def __init__(self, root, w=360, h=400):
        """
            Initialize
        :return:
        """
        super().__init__(root, width=w, height=h)   #初始化对象,同时设置高宽
        self.width = w
        self.height = h
        self.imglist = {}       #保存图片对象

    #弹窗显示描述
    def display(self, description):
        """
            The popover displays the description
        :return:
        """
        messagebox.showinfo(title='Description', message=description)

    #更新背包内容
    def udpate(self, package):
        """
            Update backpack content
        :return:
        """
        self.delete(tk.ALL)     #先清空画布
        #布置背景图
        try:
            img = ImageTk.PhotoImage(Image.open('res/package.png').resize((360, 400), Image.ANTIALIAS))   #缩放图片
            self.imglist['package'] = img    #添加图片对象到列表
            self.create_image(0, 0, image=img, anchor='nw')
        except Exception as e:
            print(str(e))
        #布置背包内容
        count = 0       #记录第几个物品
        for i in package:
            #新建物品按钮
            bt = tk.Button(self, bd=0, relief=tk.SOLID, command=partial(self.display, i.description))    #新建按钮组件
            bt_win = self.create_window(15+90*(count%4), 20+90*(count//4), window=bt, anchor='nw', width=60, height=60)      #绘制组件
            #设置物品的图片
            try:
                imgpath = 'res/thing'+str(i.type)+'.png'
##                print(imgpath)
                if os.path.exists(imgpath):
                    img = ImageTk.PhotoImage(Image.open(imgpath).resize((60, 60), Image.ANTIALIAS))   #缩放图片
                else:
                    img = ImageTk.PhotoImage(Image.open('res/thing.png').resize((60, 60), Image.ANTIALIAS))   #缩放图片
                self.imglist['thing'+str(i.id)] = img    #添加图片对象到列表,这里注意下,要用ID,不能把上一个按钮的图片对象给覆盖掉
                bt.config(image=img)    #给按钮加上图片
            except Exception as e:
                print(str(e))
            count += 1      #计数+1
        
        

    
