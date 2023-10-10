import tkinter as tk
from tkinter import ttk
import uuid
import json

with open("data.json","r") as f:
    data = json.load(f)

try:
    for k in data.keys():
        print(k)
except:
    print("couldn't find specified data")

root = tk.Tk()
root.geometry("500x500")
root.title("test")

# Import the tcl file
root.tk.call('source', 'Forest-ttk-theme-master\\forest-dark.tcl')

# Set the theme with the theme_use method
ttk.Style().theme_use('forest-dark')

label = ttk.Label(root, text="Hello World!", font=('Arial', 18, 'bold')) # create a labal
label.pack(padx=20, pady=20) # add the label, and padding

buttonFrame = tk.Frame(root)
buttonFrame.pack(padx=20, pady=20)
buttonFrame.columnconfigure(0,weight=1)
buttonFrame.columnconfigure(1,weight=10)
buttonFrame.columnconfigure(2,weight=1)

style = ttk.Style()
style.configure("Custom.TButton",padding=(10,5),anchor='w')

def popupmsg(msg):
    popup = tk.Tk()
    popup.title("Notification")
    label = ttk.Label(popup, text=msg)
    label.pack()
    popup.mainloop()

def createButton(txt):
    global btnCount
    btnLabel = tk.Label(buttonFrame,text=str(btnCount+1)+".",compound="left")
    btnLabel.grid(row=btnCount,column=0,sticky=tk.W+tk.E,pady=2)
    btn = ttk.Button(buttonFrame, style="Custom.TButton",compound="left",text=txt, command=lambda : popupmsg(txt)) 
    btn.grid(row=btnCount,column=1,sticky=tk.W+tk.E,pady=2)
    btnCount = btnCount + 1

def removeButtons():
    global btnCount
    btnCount=0
    list = buttonFrame.pack_slaves()
    for l in list:
        l.destroy()

# def switchGroup(group):
    

# # Execute Code!
# btnCount=0

print(buttonFrame)
btnCount=0
# Initial Button Population
for k in data.keys():
    val = data[k]['label']
    createButton(val)

buttonFrame.pack(fill='x')

root.mainloop() # this bit makes it render I think
