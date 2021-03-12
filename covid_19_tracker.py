from tkinter import  *
from PIL import (Image,ImageTk)
from tkinter.messagebox import *
import web_scrap
import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
import datetime

class covid_tracker:
    class ImageLabel(Label):
        """a label that displays images, and plays them if they are gifs"""
        def unload(self):
            self.config(image=None)
            self.frames = None 
            
        def next_frame(self):
            if self.frames:
                self.loc += 1
                self.loc %= len(self.frames)
                self.config(image=self.frames[self.loc])
                self.after(self.delay, self.next_frame)
            
        def load(self, im):
            if isinstance(im, str):
                im = Image.open(im)
            self.loc = 0
            self.frames = []
            try:
                for i in count(1):
                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                    im.seek(i)
            except EOFError:
                pass

            try:
                self.delay = im.info['duration']
            except:
                self.delay = 100

            if len(self.frames) == 1:
                self.config(image=self.frames[0])
            else:
                self.next_frame()
            
            
    def __init__(self,root,photo):
        #===== root functions
        self.root=root
        self.root.title('Covid-19 Tracker')
        self.root.geometry('830x600')
        self.root.resizable(False,False)
        
        #===== variables
        df=pd.read_csv('covid1.csv')
        self.index=9
        self.cn='India'
        self.total_cases=StringVar()
        self.total_cases.set('Total Cases\n'+str(df['total cases'][9]))
        self.active=StringVar()
        self.active.set('Active\n'+str(df['active cases'][9]))
        self.recovery=StringVar()
        self.recovery.set('Recovery\n'+str(df['total recovered'][9]))
        self.deaths=StringVar()
        self.deaths.set('Deaths\n'+str(df['total deaths'][9]))
        self.today=StringVar()
        self.today.set('Today\n'+str(df['new cases'][9]))
        self.photo=photo
        self.status=StringVar()
        current_date = datetime.date.today()
        current_date = current_date.strftime("%d-%B-%Y")
        self.status.set('Covid-19\nStatus Tracker\n'+current_date)
        self.sh=StringVar()
        self.sh.set('India')
        self.top_10_var=False
        
        fg_col='ghost white'
        
        self.lf=LabelFrame(self.root,text='Updates',font=('arial',14,'bold'),height=110,bd=5,bg='grey',fg=fg_col)
        self.lf.pack(fill=X)
        
        Label(self.lf,textvar=self.total_cases,font=('arial',12,'bold'),bg='tomato',fg=fg_col,padx=40,width=8).grid(row=0, column=0)
        
        Label(self.lf,textvar= self.active,font=('arial',12,'bold'),bg='DeepSkyBlue2',fg=fg_col,padx=40,width=8).grid(row=0, column=1)
        
        Label(self.lf,textvar=self.recovery,font=('arial',12,'bold'),bg='forest green',fg=fg_col,padx=40,width=8).grid(row=0, column=2)
        
        Label(self.lf,textvar=self.deaths,font=('arial',12,'bold'),bg='red2',fg=fg_col,padx=40,width=8).grid(row=0,column=3)
        
        Label(self.lf,textvar=self.today,font=('arial',12,'bold'),bg='chocolate1',fg=fg_col,padx=40,width=8).grid(row=0,column=4)
        
        lb1=Frame(self.root,bg=fg_col)
        lb1.place(x=10,y=75,width=255,height=50)
             
        Button(lb1,text='Bar',font=('arial',14),bg='blue',fg=fg_col, command=self.bar, width = 6).pack(padx=15,pady=5,side=LEFT)
        
        Button(lb1,text='Pie',font=('arial',14),bg='forest green',fg=fg_col, command=self.pie, width = 6).pack(padx=35,pady=5,side=LEFT)
        
        lb2=Frame(self.root,bg=fg_col)
        lb2.place(x=340,y=75,width=490,height=50)
        
        Label(lb2,text='Country Name',font=('arial',12),bg=fg_col,fg='red').pack(padx=10,side=LEFT)
        
        ent = Entry(lb2,width=25,textvar=self.sh,font=('arial',12))
        ent.pack(padx=5,side=LEFT)
        ent.focus_set()
         
        Button(lb2,text='Search',font=('arial',14),fg=fg_col,bg='forest green', command=self.search, width = 6).pack(padx=10,pady=5,side=LEFT)
        
        lb3=Frame(self.root,bg='chocolate1')
        lb3.place(x=10,y=130,width=300,height=455)
        
        Label(lb3,image=photo).pack(pady=10)
        
        Label(lb3,textvar=self.status,font=('arial',13,'bold'),fg=fg_col,bg='chocolate1').pack(pady=10)
        
        Button(lb3,text='Refresh', font=('arial',12),fg=fg_col,bg='forest green',width=7).pack(pady=10)
        
        Button(lb3,text='World',  font=('arial',12),fg=fg_col,bg='forest green',width=7, command=self.world).pack(pady=10)
        
        Button(lb3,text='Top 10', font=('arial',12), fg=fg_col,bg='forest green',width=7, command=self.top_10).pack(pady=10)
        
        self.lb4=Frame(self.root,bg='ghost white', relief=GROOVE,bd=12)
        self.lb4.place(x=320,y=130,width=510,height=455)
        
        lbl = self.ImageLabel(self.lb4)
        lbl.pack()
        lbl.load('Images/g4.gif')
        #showinfo('Author','Covid Tracker \nMade by B Nayak')
  
    def world(self):
        self.top_10_var=False
        self.cn='World'
        self.index=7
        i=self.index
        df=pd.read_csv('covid1.csv')
        self.total_cases.set('Total Cases\n'+str(df['total cases'][i]))
        self.active.set('Active\n'+str(df['active cases'][i]))
        self.recovery.set('Recovery\n'+str(df['total recovered'][i]))
        self.deaths.set('Deaths\n'+str(df['total deaths'][i]))
        self.today.set('Today\n'+str(df['new cases'][i]))
        
    def top_10(self):
        self.top_10_var=True
        self.x=[0,0,0,0,0]
        df=pd.read_csv('covid1.csv')
        for i in range(8,18):
            self.x[0]+=df['total cases'][i]
            self.x[1]+=df['active cases'][i]
            self.x[2]+=df['total recovered'][i]
            self.x[3]+=df['total deaths'][i]
            self.x[4]+=df['new cases'][i]
            
        self.total_cases.set('Total Cases\n'+str(self.x[0]))
        self.active.set('Active\n'+str(self.x[1]))
        self.recovery.set('Recovery\n'+str(self.x[2]))
        self.deaths.set('Deaths\n'+str(self.x[3]))
        self.today.set('Today\n'+str(self.x[4]))
        
        
    def bar(self):
        df=pd.read_csv('covid1.csv')
        i=self.index
        x=[df['total cases'][i],df['active cases'][i],df['total recovered'][i],df['total deaths'][i]]
        labels=['Total','Active','Recovered','Deaths']
        Colors=['b','#FF8000','#0080FF','#FF0000']
        
        if self.top_10_var:
            x[0]=self.x[0]
            x[1]=self.x[1]
            x[2]=self.x[2]
            x[3]=self.x[3]
            
        plt.bar(labels,x,color=Colors)
        
        if self.top_10_var:
            plt.title(f'Covid status in Top 10')
        else:
            plt.title(f'Covid status in {self.cn}')
            
        plt.show()
        
    def pie(self):
        df=pd.read_csv('covid1.csv')
        i=self.index
        x=[df['active cases'][i],df['total deaths'][i],df['total recovered'][i]]
        labels=['Active','Deaths','Recovered']
        Colors=['#FF8000','#FF0000','#0080FF']
        
        if self.top_10_var:
            x[0]=self.x[1]
            x[1]=self.x[3]
            x[2]=self.x[2]
            
        plt.pie(x,labels=labels,colors=Colors,autopct='%0.2f%%')
        
        if self.top_10_var:
            plt.title(f'Covid status in Top 10')
        else:
            plt.title(f'Covid status in {self.cn}')
            
        plt.show()
          
    def search(self):
        self.cn=self.sh.get()
        self.top_10_var=False
        df=pd.read_csv('covid1.csv')
        try:
            for i in range(8,227):
                if df['country'][i]==self.cn:
                    self.total_cases.set('Total Cases\n'+str(df['total cases'][i]))
                    self.active.set('Active\n'+str(df['active cases'][i]))
                    self.recovery.set('Recovery\n'+str(df['total recovered'][i]))
                    self.deaths.set('Deaths\n'+str(df['total deaths'][i]))
                    self.today.set('Today\n'+str(df['new cases'][i]))
                    self.index=i
                    
        except:
            pass
            #showwarning('Oops!!',"First letter must be captial \n\tor\nYou enter a illegal country name")
        
        
def main(root,photo):
        obj=covid_tracker(root,photo)
        
if __name__=='__main__':
    root=Tk()  
    image=Image.open('Images/corona.png'). resize(( 280,140))
    photo=ImageTk.PhotoImage(image)
    main(root,photo)
    root.mainloop()