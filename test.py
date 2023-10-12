import tkinter as tk
from tkinter import ttk
import uuid
import json
import pyperclip as pc

with open("data.json","r") as f:
    data = json.load(f)

# try:
#     for k in data.keys():
#         print(k)
# except:
#     print("couldn't find specified data")

root = tk.Tk()
root.geometry("500x500")
root.title("test")

# Import the tcl file
root.tk.call('source', 'Forest-ttk-theme-master\\forest-dark.tcl')

# Set the theme with the theme_use method
ttk.Style().theme_use('forest-dark')

label = ttk.Label(root, text="Snippet Stockpile", font=('Arial', 18, 'bold')) # create a labal
label.pack(padx=20, pady=20) # add the label, and padding

controlFrame = tk.Frame(root)
controlFrame.pack(padx=20,pady=10)
controlFrame.columnconfigure(0,weight=1)
controlFrame.columnconfigure(1,weight=1)
controlFrame.columnconfigure(2,weight=1)
controlFrame.columnconfigure(3,weight=1)
buttonFrame = tk.Frame(root)
buttonFrame.pack(padx=20, pady=10)
buttonFrame.columnconfigure(0)
buttonFrame.columnconfigure(1,weight=1)
buttonFrame.columnconfigure(2)

style = ttk.Style()
style.configure("Custom.TButton",padding=(10,5),anchor='w')

def popupmsg(msg):
    popup = tk.Tk()
    popup.title("Notification")
    label = ttk.Label(popup, text=msg)
    label.pack()
    popup.mainloop()

def createButton(buttonID):
    global btnCount

    # LABEL
    txt = data[buttonID]['label']
    btnLabel = tk.Label(buttonFrame,text=str(btnCount+1)+".",compound="left")
    btnLabel.grid(row=btnCount,column=0,sticky=tk.W+tk.E,pady=2)
    
    # COMMAND
    if (data[buttonID]['group']):
        btn = ttk.Button(buttonFrame, style="Custom.TButton",compound="left",text=txt, command=lambda : switchGroup(buttonID)) 
    else:
        content = data[buttonID]['content']
        btn = ttk.Button(buttonFrame, style="Custom.TButton",compound="left",text=txt, command=lambda : popupmsg(content)) 
    
    btn.grid(row=btnCount,column=1,sticky=tk.W+tk.E,pady=2)
    btnCount = btnCount + 1

def removeButtons():
    global btnCount
    btnCount=0
    print('buttonFrame children',buttonFrame.winfo_children())
    for widgets in buttonFrame.winfo_children():
        widgets.destroy()

def switchGroup(groupID):
    # print(groupID)
    removeButtons()
    for k in data.keys():
        if (data[k]['parent']==groupID):
            createButton(k)

def createBackButton(grandParentID):
    if (grandParentID == ""):
        createFirstGroupButtons()
    else:
        createGroupButtons(grandParentID)

def createFirstGroupButtons():
    for k in data.keys():
        if (data[k]['parent'] == ""):
            createButton(k)

def createGroupButtons(groupID):
    for k in data.keys():
        if (data[k]['parent'] == groupID):
            createButton(k)

# Initial Button Population
btnCount=0
buttonFrame.pack(fill='x')
createFirstGroupButtons()
root.mainloop() # this bit makes it render
