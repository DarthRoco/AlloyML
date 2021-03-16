import tensorflow as tf
import pygad
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import constants
from PIL import Image, ImageTk
import ga
import threading
import numpy as np
import time
from tkinter import messagebox



#Use these values while trying to get decent answer in decent runtime
# TARGET=347
# MODEL='ys'
# vars=['S','Cu','Nb','Exit temperature']

#The Parameters we wish to provide option to user for optimisation
PARAMETERS=['Furnace temperature', 'Exit temperature', 'Annealing temperature',
            'Sulphur', 'Copper', 'Nickel', 'Chromium', 'Molybdenum', 'Niobium', 'Aluminium(Total)',
            'Tin', 'Arsenic', 'Calcium', 'Lead', 'Carbon(Eq1)', 'Carbon(Eq2)', 'Vanadium', 'Titanium',
            'Antimony', 'Zirconium', 'Nitrogen', 'Boron', 'Oxygen']

#loads corresponding model from memory
def load_models(opn):
    if opn=='el':
        model = tf.keras.models.load_model('models/el.h5')
    elif opn=='ts':
        model = tf.keras.models.load_model('models/ts.h5')
    elif opn=='ys':
        model = tf.keras.models.load_model('models/ys.h5')
    return model

#Create Root Window
root=tk.Tk()
root.title('Alloy Compose')

#Create Title
welcometext=tk.Label(root,text="ISTE CLUTCH ALLOY RECOMMENDATION SYSTEM",padx=10,pady=10,fg="blue",font=25)
welcometext.pack()

#Create frame to insert options
frame=tk.Frame(root,borderwidth=5)
frame.pack(padx=50,pady=50)

#Create Dropdown for Required Property
options=[
    'Yield Strength',
    'Yield Strength',
    'Tensile Strength',
    'Elongation Limit']
dropdown=tk.StringVar()
drop=OptionMenu(frame,dropdown,*options) 
drop.grid(row=1,column=0)

space=Label(frame,text="                         ")
space.grid(row=1,column=1)

#Create Input Box to accept Target Value
tgr=tk.Label(frame,text="REQUIRED VALUE:")
tgr.grid(row=1,column=2)
e=tk.Entry(frame)
e.grid(row=1,column=3)
intvar_dict = {}


#Create an array of checkboxes for various compositions user may want to optimise
checkbutton_list = []
row,col=2,0
frame2=Frame(frame)
frame2.grid(row=2,column=0,columnspan=4)
for key in PARAMETERS:
    intvar_dict[key]=IntVar()
    c=Checkbutton(frame2,text=key,variable=intvar_dict[key])
    c.grid(row=row,column=col)
    col+=1
    if (col+1)%4==0:
        col=0
        row+=1
    checkbutton_list.append(c)

warn=tk.Label(frame,text='Note checking any of the below boxes will significantly increase runtime.It is recomended NOT to use them unless absolutely neccessary',fg="red")
warn.grid(row=3,column=0,columnspan=4)

#Extra Functionality in case of low convergence
converge=IntVar()
complex=Checkbutton(frame,text='Check this box if GA failed to converge',variable=converge)
complex.grid(row=4,column=0,columnspan=2)

#Extra Functionality in case one wants to get more accurate results
acc=IntVar()
accurate=Checkbutton(frame,text='Check this box for greater precision in answer',variable=acc)
accurate.grid(row=4,column=2,columnspan=2)

image1 = Image.open("media/iste.jpg")
image2 = image1.resize((100, 100), Image.ANTIALIAS)
test = ImageTk.PhotoImage(image2)

label1 = tk.Label(image=test)
label1.image = test

# Position image
label1.place(x=0, y=0)

#Primary Function,Called when optimize button is pressed.Processes user input and passes to GAsolver.
#Also displays results in new window
def test():
    vararr=[]
    for key, value in intvar_dict.items():
        if value.get() > 0:
            vararr.append(key)
    for key, value in intvar_dict.items():
        value.set(0)
    try:
        TARGET=float(e.get())
    except:
        TARGET=""
    mode=dropdown.get()

    if mode==options[1]:
        MODEL='ys'

    elif mode==options[2]:
        MODEL='ts'
    elif mode==options[3]:
        MODEL='el'
    e.delete(0,END)

    accure=acc.get()
    if accure==0:
        ACC=100
    elif accure>=1:
        ACC=800
        COMP=35

    comp=converge.get()
    if comp>=1:
        COMP=50
    elif comp==0:
        COMP=20


    if (TARGET=="" )or (MODEL==None):
        messagebox.showerror("Error","Please select a target value")
    elif (len(vararr)==0):
        messagebox.showerror("Error", "Please select at least one parameter to optimize")

    else:
        top=Toplevel()
        top.title('Result')
        wait=Label(top,text="Please wait while computation is ongoing....")
        wait.pack()
        #Progress Bar
        my_progress=ttk.Progressbar(top, orient="horizontal",length=300,mode='indeterminate')
        my_progress.pack(pady=20)
        my_progress.start(10)
        btw=tk.Button(top,text="close",command=top.destroy,borderwidth=5).pack()
        star=time.time()
        ans=ga.ga_solver(TARGET,vararr,MODEL,COMP,ACC)
        k = []
        for key in ans[1]:
            k.append(ans[1][key])
        k=np.asarray(k)
        
        k=np.reshape(k,(1,26))
        
        model=load_models(MODEL)
        an=model.predict(k)
        
        my_progress.stop()
        my_progress.destroy()
        wait.config(text=f"The operation took roughly {int((time.time()-star)/60)+1} minutes.Here are the results")

        ss=dict(ans[0])
        
        table=ttk.Treeview(top,columns=('Property','Value'),show='headings',height=26)
        for col in ('Property','Value'):
            table.heading(col,text=col)
        for i,(key,value) in enumerate(ss.items()):
            table.insert("","end",values=(key,round(value,5)))
        table.pack()
        trg=Label(top,text=f"The Target was {TARGET}")
        pred=Label(top,text=f"The GA acheived {an[0][0]}")
        trg.pack()
        pred.pack()



#Threading so as to prevent gui lockup
def step():
    threading.Thread(target=test).start()

#Primary button,triggers GA
btn1 =tk.Button(root, text="Optimize", command=step,borderwidth= 5)
btn1.pack()



#Main loop
root.mainloop()