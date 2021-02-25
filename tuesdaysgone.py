import numpy as np
import pandas as pd
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import IntVar, Tk, Frame, Label, LabelFrame, Button, Checkbutton, Entry, Canvas, Scrollbar, Text, ttk, Listbox
import csv

##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################

# SET UP WINDOW
root = Tk()

# GLOBAL VARIABLES
global currentIndex
currentIndex = 0
global skipVar
global cartList
cartList = []
global end_pos
end_pos = ''
global start_pos
start_pos = 0
global numInfo
global idInfo
global wordInfo
global gameDescInfo
global gameDescTxt
global searchInput
global searchCanvas
global searchListBox
global checkBoxes
checkBoxes = []
global cartCanvas
global cartListBox
global cartCheckBoxes
cartCheckBoxes = []
global change_array
change_array = []
global list_of_games

# METHODS
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = "black"
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.configure(background = "black", 
                        foreground="white", 
                        activebackground = "grey66", 
                        font=('Consolas', 12),
                        padx=2, pady=2)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

# FUNCTIONS
def prev_row():
    global currentIndex
    if currentIndex > 0:
        currentIndex = currentIndex - 1
    destroy_info()
    update_info()

def next_row():
    global currentIndex
    global CurrentGameId
    keepSkipping = True
    skipNum = 0
    count = 0
    
    if currentIndex < len(df.index):
        if df.iloc[currentIndex + 1].id == df.iloc[currentIndex].id:
            while keepSkipping == True:
                count += 1
                if df.iloc[currentIndex + count].id == df.iloc[currentIndex].id:
                    skipNum+=1
                else:
                    keepSkipping = False        
        
        currentIndex = currentIndex + 1 +skipNum



    destroy_info()
    update_info()
    
def destroy_info():
    global numInfo
    global idInfo
    global gameDescInfo
    global gameDescTxt

    numInfo.destroy()
    idInfo.destroy()
    gameDescInfo.destroy()
    gameDescTxt.delete('1.0', tk.END)
    backMatchBox.delete('1.0', tk.END)

def update_info():
    global numInfo
    global idInfo
    global gameDescInfo
    global gameDescTxt
    global current_game_df

    numInfo = Label(frame1, text=df.iloc[currentIndex].game_num)
    numInfo.place(x=10, y=35)
    numInfo.configure(background = "black", foreground="white", font=('Consolas', 12))
    idInfo = Label(frame1, text=df.iloc[currentIndex].id)
    idInfo.place(x=150, y=35)
    idInfo.configure(background = "black", foreground="white", font=('Consolas', 12))   
    gameDescInfo = Label(frame1, text=df.iloc[currentIndex].game_name)
    gameDescInfo.place(x=300, y=35)
    gameDescInfo.configure(background = "black", foreground="white", font=('Consolas', 12))
    gameDescTxt.insert(1.0, "{}".format(df.iloc[currentIndex].game_description), 'warning')

    currentGameId = df.iloc[currentIndex].id
    current_game_df = df[['id','word','changed_word2','std_word']]
    current_game_df = current_game_df.loc[current_game_df['id'] == currentGameId]

    backMatchBox.insert(1.0, "{}".format(current_game_df))


    highlight_word()

def highlight_word():

    currentGameWordList = current_game_df['word']
    for w in currentGameWordList:
        print(w.replace("_"," "))

        global start_pos
        start_pos = 0
        global end_pos
        end_pos = ''
        #gameDescTxt.delete('1.0', tk.END)
        #gameDescTxt.insert(1.0, df.iloc[currentIndex].game_description, 'warning')
        #h_word = df.iloc[currentIndex].word.replace(" ","_")
        h_word = w.replace(" ","_")
        h_word = w.strip()
        start_pos = gameDescTxt.search(h_word, '1.0', stopindex=tk.END)
        if not start_pos:   #in case the word is capitalized b/c it's first word in sentence
            start_pos = gameDescTxt.search(h_word.capitalize(), '1.0', stopindex=tk.END)
        if not start_pos:   #in case the word is all uppercase letters  
            start_pos = gameDescTxt.search(h_word.upper(), '1.0', stopindex=tk.END)
        if not start_pos:   #in case the word has hyphens
            start_pos = gameDescTxt.search(h_word.replace(" ","-"), '1.0', stopindex=tk.END)
        if start_pos:
            if end_pos:
                gameDescTxt.tag_remove('highlight', start_pos, end_pos)
            end_pos = '{}+{}c'.format(start_pos, len(h_word))            
            gameDescTxt.tag_add('highlight', start_pos, end_pos)
            gameDescTxt.tag_config('highlight', background='yellow', foreground = "black")

def load_file():
    global df
    global currentGameId
    df = pd.read_csv('{}.csv'.format(loadFileInput.get()), index_col ="index")
    df = df.astype({"id": int, 
                    "game_num": int, 
                    "word": str, 
                    "game_name": str, 
                    "game_description": str,
                    "stemmed_word": str,
                    "changed_word": str, 
                    "remark": str, 
                    "std_word": str,
                    "occurances": int})      
    
    df = df.sort_values(['id', 'std_word'], ascending=[True, False])

    df.reset_index(inplace=True)

    currentGameId = df.iloc[0].id

    update_info()   

##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################

# SET WINDOW SIZE
rootWidth = 1800
rootHeight = 900
root.geometry('{}x{}+40+40'.format(rootWidth, rootHeight))
root.resizable(width=False, height=False)

# SET FRAME DIMENSIONS
frame1 = Frame(root, width=900, height=900)
frame1.place(x=0,y=0)
frame1.config(bg="grey11")
frame2 = Frame(root, width=900, height=900)
frame2.place(x=900,y=0)
frame2.config(bg="grey22")

# FRAME 1
numTitle = Label(frame1, text="Game number:")
numTitle.place(x=10, y=10)
numTitle.configure(background = "black", foreground="white", font=('Consolas', 12))
numInfo = Label(frame1, text="")
numInfo.place(x=10, y=35)
numInfo.configure(background = "black", foreground="white", font=('Consolas', 12))
idTitle = Label(frame1, text="Game ID:")
idTitle.place(x=150, y=10)
idTitle.configure(background = "black", foreground="white", font=('Consolas', 12))
idInfo = Label(frame1, text="")
idInfo.place(x=150, y=35)
idInfo.configure(background = "black", foreground="white", font=('Consolas', 12))
gameDescTitle = Label(frame1, text="Game:")
gameDescTitle.place(x=300, y=10)
gameDescTitle.configure(background = "black", foreground="white", font=('Consolas', 12))
gameDescInfo = Label(frame1, text="")
gameDescInfo.place(x=300, y=35)
gameDescInfo.configure(background = "black", foreground="white", font=('Consolas', 12))

prevBtn= HoverButton(frame1, text="Previous", command=prev_row, padx=2, pady=2)
prevBtn.place(x=10,y=75)
nextBtn = HoverButton(frame1, text="Next", command=next_row, padx=2, pady=2)
nextBtn.place(x=100,y=75)

loadFileBtn = HoverButton(frame1, text="Load", command=load_file)
loadFileBtn.place(x=410,y=75)
loadFileInput = Entry(frame1, width=42, justify = "left", font=('Consolas', 12))
loadFileInput.place(x=475,y=79)
loadFileInput.configure(background = "black", foreground="white", font=('Consolas', 12))

gameDescTxt = st.ScrolledText(frame1, undo=True, width=70, height=31, wrap="word", bg = "black", fg = "white", font=('Consolas', 16))
gameDescTxt.place(x=5, y=120)
gameDescTxt.insert(1.0, "LOAD A FILE..")

#FRAME 2
backMatchCanvas = Frame(frame2, bg='grey22', width=880, height=950)
backMatchCanvas.place(x=5,y=5)
backMatchBox = st.ScrolledText(backMatchCanvas, width=100, height=46, wrap="none")
backMatchBox.configure(background = "black", foreground="white", font=('Consolas', 12))
backMatchBox.place(x=5,y=5)

# MAIN LOOP
root.mainloop()