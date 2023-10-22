import tkinter as tk
from tkinter import ttk
import uuid
import json
import pyperclip as pc

# Globals =====================================================================================
btnCount=0

# Main =====================================================================================
def main():
# =====================================================================================
# FUNCTIONS =====================================================================================
# ==========================================================================================
    def popupmsg(msg):
        popup = tk.Tk()
        popup.title("Notification")
        label = ttk.Label(popup, text=msg)
        label.pack()
        popup.mainloop()

    def removeButtons():
        global btnCount
        btnCount=0
        for widgets in buttonFrame.winfo_children():
            widgets.destroy()
        for widgets in controlFrame.winfo_children():
            widgets.destroy()
        for widgets in controlFrame2.winfo_children():
            widgets.destroy()
        
    def switchGroup(buttonID):
        removeButtons()
        createGroupButtons(buttonID)

    def backButton(groupID=""):
        global data
        removeButtons()
        if groupID:
            parentID = data[groupID]['parent']
            if (parentID != ""):
                grandParentID = data[parentID]['parent']
            else:
                grandParentID = ""
            if (grandParentID == ""):
                createFirstGroupButtons()
            else:
                createGroupButtons(grandParentID)
        else:
            createFirstGroupButtons()
            
#################################################################################################################################
# CREATE BUTTONS ################################################################################################################ 
#################################################################################################################################
    def createButton(buttonID):
        global btnCount
        global data
        # INCREMENT COUNT
        btnCount = btnCount + 1

        # LABEL
        txt = data[buttonID]['label']
        btnLabel = tk.Label(buttonFrame,text=str(btnCount)+".",compound="left")
        btnLabel.grid(row=btnCount-1,column=0,sticky=tk.W+tk.E,pady=2)

        # EDIT BUTTON
        editBtn = ttk.Button(buttonFrame, text="🖊",style="Center.TButton",width=0,command=lambda:createForm(buttonID))
        editBtn.grid(row=btnCount-1,column=2,pady=2,padx=4)
        
        # BUTTON WITH COMMAND
        if (data[buttonID]['group']):                                   # GROUP BUTTON
            btn = ttk.Button(buttonFrame, style="Custom.TButton",compound="left",text=txt, command=lambda : switchGroup(buttonID)) 
        else:                                                           # COPY TEXT BUTTON
            content = data[buttonID]['content']
            btn = ttk.Button(buttonFrame, style="Custom.TButton",compound="left",text=txt, command=lambda : pc.copy(content))
        root.bind(btnCount, lambda event, button=btn: btn.invoke()) # I don't understand why this works but it does
        btn.grid(row=btnCount-1,column=1,sticky='we',pady=2)

    def createAddButton():
        btn = ttk.Button(controlFrame, text="Add", command=lambda : createForm())
        btn.grid(row=0,column=0,padx=0,sticky="W")

    def createOptionsButton():
        btn = ttk.Button(controlFrame, text="Options", command=lambda : popupmsg("test"))
        btn.grid(row=0,column=1,padx=10,sticky="W")

    def createBackButton(grandParentID=""):
        if grandParentID:
            btn = ttk.Button(controlFrame2, text="Back", command=lambda : backButton(grandParentID))
        else:
            btn = ttk.Button(controlFrame2, text="Back", command=lambda : backButton())
        root.bind('b',lambda event, button=btn: btn.invoke())
        btn.grid(row=0,column=0,sticky="E")

    # def createSpacer():
    #     spacer_label = ttk.Label(controlFrame, text="", width=10)
    #     spacer_label.grid(row=0, column=0)

    def createFirstGroupButtons():
        global data
        createControlButtons()
        if data:
            for k in data.keys():
                if (data[k]['parent'] == ""):
                    createButton(k)

    def createGroupButtons(groupID):
        global data
        createControlButtons()
        if data:
            if (data[groupID]['group']):
                createBackButton(groupID)
                for k in data.keys():
                    if (data[k]['parent'] == groupID):
                        createButton(k)
            #further logic to come for action when not a group?

    def createControlButtons():
        # createSpacer()
        createAddButton()
        createOptionsButton()

    def createSubmitButton(buttonID,e1,e2,parentID):
        btn = ttk.Button(controlFrame,text="Submit",command=lambda: submitForm(buttonID,e1,e2,parentID))
        btn.grid(row=0,column=0)
# ==========================================================================================
# NEW/EDIT DATA FORM  ======================================================================
# ==========================================================================================
    def createForm(buttonID=""):
        global data
        removeButtons()
        buttonName=""
        buttonContent=""
        group = False
        parentID=""
        chkvar=tk.IntVar()
        chkvar.set(0)
        if buttonID:
            buttonName=data[buttonID]['label']
            buttonContent=data[buttonID]['content']
            parentID = data[buttonID]['parent']
            if (data[buttonID]['group']):
                group=True
                chkvar.set(1)
        else:
            newID = uuid.uuid1()
            buttonID = newID
                        
        def checkboxFunction():
            global group
            if(chkvar.get()==0):
                e2.config( state ='enabled') 
                group = False
            elif(chkvar.get()==1):
                e2.config( state ='disabled') 
                group = True
                
        l1 = tk.Label(buttonFrame,text="Button Name: ")
        e1 = ttk.Entry(buttonFrame,width=100)
        e1.insert(0,buttonName)
        l2 = tk.Label(buttonFrame,text="Content: ")
        e2 = ttk.Entry(buttonFrame,width=100)
        e2.insert(0,buttonContent)
        l3 = tk.Label(buttonFrame,text="Button Group: ")
        ch = ttk.Checkbutton(buttonFrame,variable=chkvar, onvalue=1, offvalue=0, command=checkboxFunction)
        l4 = tk.Label(buttonFrame,text="Location: ")
        dp = tk.Listbox(buttonFrame)
    
    # position form elements
        l1.grid(row=0,column=0,sticky="E")
        e1.grid(row=0,column=1,sticky="W",columnspan=3)
        
        l2.grid(row=1,column=0,sticky="E")
        e2.grid(row=1,column=1,sticky="W",columnspan=3)
        
        l3.grid(row=2,column=0,sticky="E")
        ch.grid(row=2,column=1,sticky="W")
        
        l4.grid(row=3,column=0,sticky="NE")
        dp.grid(row=3,column=1,sticky="W")
        createSubmitButton(buttonID,e1,e2,parentID)
        createBackButton()

    def submitForm(buttonID,e1,e2,parentID):
        global data
        data[buttonID]["parent"]=parentID

        if parentID:
            data[buttonID]["group"]=True
        else:
            data[buttonID]["group"]=False
        data[buttonID]["label"]=e1.get()
        data[buttonID]["content"]=e2.get()
        print("test1",type(data))
        writeData(data) 
        

# ==========================================================================================
# SETUP AND LAUNCH =========================================================================
# ==========================================================================================
    data = dict()
    
    def readData():
        global data
        with open("data.json","r") as f:
            data = json.load(f)
            
    def writeData(data):
        print(type(data))
        json_data = json.dumps(data,indent=4)
        print(type(json_data))
        with open("data.json","w", encoding='utf-8') as json_file:
            json_file.write(json_data)
            
    readData()
    print(data)
    root = tk.Tk()
    root.geometry("500x500")
    root.title("test")

    # Import the tcl file
    root.tk.call('source', 'Forest-ttk-theme-master\\forest-dark.tcl')
    
    # Configure root to expand in both rows and columns
    root.rowconfigure(0)
    root.rowconfigure(1)
    root.grid_columnconfigure(0, weight=1)
    
    # Set the theme with the theme_use method
    ttk.Style().theme_use('forest-dark')

    header = tk.Frame(
                root, 
        # borderwidth=1, 
        # relief="solid"
    )
    header.grid(
        row=0,
        column=0, 
        padx=10, 
        pady=10, 
        sticky="nsew"
    )
    header.columnconfigure(0, weight=1)
    
    body = tk.Frame(
                root, 
        # borderwidth=1, 
        # relief="solid"
    )
    body.grid(
        row=1,
        column=0, 
        padx=10, 
        pady=10, 
        sticky="nsew"
    )
    body.columnconfigure(0, weight=1)
    
    label = ttk.Label(
        header, 
        text="Snippet Stockpile", 
        font=('Arial', 18, 'bold'), 
        # borderwidth=1, 
        # relief="solid"
    )
    label.grid(row=0, column=0, padx=10, pady=10)

    controlFrame = tk.Frame(
        body,
        width=100,
        # borderwidth=1, 
        # relief="solid"
    )
    controlFrame.grid(
        row=1,
        column=0, 
        padx=10, 
        pady=10, 
        sticky="w"
    )
    controlFrame.columnconfigure(0,weight=1)
    controlFrame.columnconfigure(1,weight=1)
    controlFrame.columnconfigure(2,weight=1)
    controlFrame.columnconfigure(3,weight=1)

    controlFrame2=tk.Frame(
        body
    )
    controlFrame2.grid(
        row=1,
        column=1,
        sticky='e'
    )
    
    buttonFrame = tk.Frame(
        body, 
        # borderwidth=1, 
        # relief="solid"
    )
    buttonFrame.grid(
        row=2, 
        column=0,
        columnspan=2,
        padx=10, 
        pady=10, 
        sticky="ew"
    )
    buttonFrame.grid_columnconfigure(0)
    buttonFrame.grid_columnconfigure(1,weight=1)
    buttonFrame.grid_columnconfigure(2)

    style = ttk.Style()
    style.configure("Custom.TButton",anchor='w')
    style.configure("Center.TButton",anchor='w',padding=(5,1,5,5))

    # BUTTON LOGIC
    root.bind('<Escape>', quit)

    # Initial Button Population
    
    createFirstGroupButtons()
    # createBindings()
    root.mainloop() # this bit makes it render#

if __name__ == '__main__':
    main()
