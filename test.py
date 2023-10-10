import tkinter as tk
from tkinter import ttk
import json

data = ""
with open("data.json","r") as data:
    data = data.read()

print(data)

root = tk.Tk()
root.geometry("500x500")
root.title("test")

# Import the tcl file
root.tk.call('source', 'Forest-ttk-theme-master\\forest-dark.tcl')

# Set the theme with the theme_use method
ttk.Style().theme_use('forest-dark')

label = tk.Label(root, text="Hello World!", font=('Arial', 18, 'bold')) # create a labal
label.pack(padx=20, pady=20) # add the label, and padding

# textbox = tk.Text(root, height=3, font=('Arial',16)) # create a text input box
# textbox.pack(padx=20)

buttonFrame = tk.Frame(root)
buttonFrame.pack(padx=20, pady=20)
buttonFrame.columnconfigure(0,weight=1)
buttonFrame.columnconfigure(1,weight=11)

def popupmsg(msg):
    popup = tk.Tk()
    popup.title("Notification")
    label = tk.Label(popup, text=msg)
    label.pack()
    popup.mainloop()

def createButton(txt):
    global btnCount
    btnLabel = tk.Label(buttonFrame,text=txt+".")
    btnLabel.grid(row=btnCount,column=0,sticky=tk.W+tk.E,pady=2)
    btn = ttk.Button(buttonFrame, text=txt, command=lambda : popupmsg(txt)) # ttk styled button
    # btn = tk.Button(buttonFrame, text=txt,font=('Arial',12), command=lambda : popupmsg(txt))
    btn.grid(row=btnCount,column=1,sticky=tk.W+tk.E,pady=2)
    btnCount = btnCount + 1

btnCount=0
createButton("1")
createButton("2")
createButton("3")
createButton("4")
# btn1 = tk.Button(buttonFrame, text="1",font=('Arial', 12))
# btn1.grid(row=0,column=0,sticky=tk.W+tk.E)

# btn2 = tk.Button(buttonFrame, text="2",font=('Arial', 12))
# btn2.grid(row=0,column=1,sticky=tk.W+tk.E)

# btn3 = tk.Button(buttonFrame, text="3",font=('Arial', 12))
# btn3.grid(row=0,column=2,sticky=tk.W+tk.E)

# btn4 = tk.Button(buttonFrame, text="4",font=('Arial', 12))
# btn4.grid(row=1,column=0,sticky=tk.W+tk.E)

# btn5 = tk.Button(buttonFrame, text="5",font=('Arial', 12))
# btn5.grid(row=1,column=1,sticky=tk.W+tk.E)

# btn6 = tk.Button(buttonFrame, text="6",font=('Arial', 12))
# btn6.grid(row=1,column=2,sticky=tk.W+tk.E)

buttonFrame.pack(fill='x')

root.mainloop() # this bit makes it render I think
