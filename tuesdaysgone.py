import numpy as np
import pandas as pd
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import IntVar, Tk, Frame, Label, LabelFrame, Button, Checkbutton, Entry, Canvas, Scrollbar, Text, ttk, Listbox, messagebox
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
global idInfo
global word_label
global std_label
global rmk_label

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
def jump_to_index():
    global currentIndex

    currentIndex = int(jumpToInput.get())

    destroy_info()
    update_info()
    update_std_words()

def prev_row():
    global currentIndex
    global currentGameId

    keepSkipping = True
    skipNum = 0
    count = 0

    if currentIndex > 0:
        if df.iloc[currentIndex - 1].id == df.iloc[currentIndex].id:
            while keepSkipping == True:
                count -= 1
                if df.iloc[currentIndex + count].id == df.iloc[currentIndex].id:
                    skipNum+=1
                else:
                    keepSkipping = False        
        
        currentIndex = currentIndex - (1 +skipNum)

    destroy_info()
    update_info()
    update_std_words()

def next_row():
    global currentIndex
    global currentGameId
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
    update_std_words()
    
def destroy_info():
    global numInfo
    global idInfo
    global gameDescInfo
    global gameDescTxt
    global searchCanvas
    global searchListBox

    numInfo.destroy()
    idInfo.destroy()
    gameDescInfo.destroy()
    gameDescTxt.delete('1.0', tk.END)
    #backMatchBox.delete('1.0', tk.END)

    searchCanvas.destroy()
    searchListBox.destroy()


def update_info():
    global numInfo
    global idInfo
    global gameDescInfo
    global gameDescTxt
    global current_game_df
    global hoverList
    global matchCase
    global std_list
    global std_spacing
    global labelList
    global rmk_spacing
    global remark_list
    global hoverList
    global idInfo
    global searchCanvas
    global searchListBox
    global input_list
    global matchDf
    global currentGameId
    global chg_spacing

    numInfo = Label(frame1, text=df.iloc[currentIndex].game_num)
    numInfo.place(x=10, y=35)
    numInfo.configure(background = "black", foreground="white", font=('Consolas', 12))
    idInfo = Label(frame1, text=df.iloc[currentIndex].id)
    idInfo.place(x=150, y=35)
    idInfo.configure(background = "black", foreground="white", font=('Consolas', 12))   
    gameDescInfo = Label(frame1, text=df.iloc[currentIndex].game_name)
    gameDescInfo.place(x=300, y=35)
    gameDescInfo.configure(background = "black", foreground="white", font=('Consolas', 12))
    description = str(df.iloc[currentIndex].game_description).replace("_"," ").lower()
    description = description.replace("."," ")
    description = description.replace('"',' ')
    description = description.replace('!',' ')
    description = description.replace(',',' ')
    description = description.replace('?',' ')
    gameDescTxt.insert(1.0, description, 'warning')

    currentGameId = df.iloc[currentIndex].id
    current_game_df = (df[['id','index','word','std_word', 'remark', 'duplicate']])
    current_game_df = current_game_df.loc[current_game_df['id'] == currentGameId]

    current_game_df = current_game_df.sort_values("index")

    test_desc = str(df.iloc[currentIndex].game_description).replace("_"," ").lower()
    test_desc = test_desc.replace("."," ")
    test_desc = test_desc.replace('"',' ')
    test_desc = test_desc.replace('!',' ')
    test_desc = test_desc.replace(',',' ')
    test_desc = test_desc.replace('?',' ')
    # print(test_desc)

    desc_word_list = test_desc.split(" ")
    # print(desc_word_list)

    # backMatchBox.insert(1.0, "{}".format(current_game_df))

    matchDf = current_game_df.loc[current_game_df['id'] == currentGameId]
    matchDf = (current_game_df[['id','word','index','std_word', 'remark', 'duplicate']]) 
    
    werd_order = []
    werds = []

    for werd in matchDf['word']:
        werd = werd.replace("."," ")
        werd = werd.replace('"',' ')
        werd = werd.replace('!',' ')
        werd = werd.replace(',',' ')
        werd = werd.replace('?',' ')
        lower_werd = werd.lower().split(" ")[0]

        if lower_werd in desc_word_list:
            werd_order.append(desc_word_list.index(lower_werd))
            werds.append(lower_werd)
        else:
            werds.append("na")
            werd_order.append(99)
        
    
    
    matchDf['order'] = werd_order
    matchDf = matchDf.sort_values('order')
    matchList = []
    matchDf['new_werd_order'] = np.arange(len(matchDf))

    searchCanvas = Canvas(frame2, bg='black', width=375, height=900)
    searchCanvas.place(x=5,y=60)
    searchListBox = st.ScrolledText(searchCanvas, width=144, height=52, wrap="none")
    searchListBox.configure(background = "black")
    searchListBox.pack() 

    print(matchDf)

    for i in range(len(matchDf)):
        # matchList.append(matchDf[i])
        matchList = matchDf.values.tolist()

    labelList = []
    hoverList = []
    std_list = []
    std_spacing = []
    rmk_spacing = []
    remark_list = []
    input_list = []
    chg_butt = []
    chg_spacing = []

    for matchCase in range(len(matchList)):
        labelList.append(Label(searchListBox, text=matchList[matchCase][1].replace("_"," ")))
        # labelList[matchCase].changed_word = matchList[matchCase]
        labelList[matchCase].config(background = "black", foreground= 'white', font = ('Consolas', 12, 'bold'))
        labelList[matchCase].bind("<Enter>", on_enter)
        labelList[matchCase].bind("<Leave>", on_leave)
        labelList[matchCase].word = matchList[matchCase]
        labelList[matchCase].number = matchCase

        # hoverList.append(Label(searchListBox, text="HOVER OVER TO SEE DESCRIPTIONS   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX "))
        hoverList.append(Label(searchListBox, text="XXXX"))
        hoverList[matchCase].word = matchList[matchCase]
        hoverList[matchCase].number = matchCase
        hoverList[matchCase].config(background = "black", foreground= 'black', font = ('Consolas', 12))
        hoverList[matchCase].bind("<Enter>", on_enter)
        hoverList[matchCase].bind("<Leave>", on_leave)
        
        std_space_len = 32 - len(matchList[matchCase][1])
        rmk_space_len = 32 - len(matchList[matchCase][3])
        chg_space_len = 22 - len(matchList[matchCase][4])

        std_spacing.append(Label(searchListBox, text= "x" * std_space_len))
        std_spacing[matchCase].config(background = "black", foreground= 'black', font = ('Consolas', 12, 'bold'))
        std_spacing[matchCase].bind("<Enter>", on_enter)
        std_spacing[matchCase].bind("<Leave>", on_leave)
        std_spacing[matchCase].word = matchList[matchCase]
        std_spacing[matchCase].number = matchCase

        std_list.append(Label(searchListBox, text=matchList[matchCase][3]))
        std_list[matchCase].config(background = "black", foreground= 'white', font = ('Consolas', 12, 'bold'))
        std_list[matchCase].bind("<Enter>", on_enter)
        std_list[matchCase].bind("<Leave>", on_leave)
        std_list[matchCase].word = matchList[matchCase]
        std_list[matchCase].number = matchCase

        rmk_spacing.append(Label(searchListBox, text= "x" * rmk_space_len))
        rmk_spacing[matchCase].config(background = "black", foreground= 'black', font = ('Consolas', 12, 'bold'))
        rmk_spacing[matchCase].bind("<Enter>", on_enter)
        rmk_spacing[matchCase].bind("<Leave>", on_leave)
        rmk_spacing[matchCase].word = matchList[matchCase]
        rmk_spacing[matchCase].number = matchCase

        remark_list.append(Label(searchListBox, text=matchList[matchCase][4]))
        remark_list[matchCase].config(background = "black", foreground= 'white', font = ('Consolas', 12, 'bold'))
        remark_list[matchCase].bind("<Enter>", on_enter)
        remark_list[matchCase].bind("<Leave>", on_leave)
        remark_list[matchCase].word = matchList[matchCase]
        remark_list[matchCase].number = matchCase

        chg_spacing.append(Label(searchListBox, text= "x" * chg_space_len))
        chg_spacing[matchCase].config(background = "black", foreground= 'black', font = ('Consolas', 12, 'bold'))
        chg_spacing[matchCase].bind("<Enter>", on_enter)
        chg_spacing[matchCase].bind("<Leave>", on_leave)
        chg_spacing[matchCase].word = matchList[matchCase]
        chg_spacing[matchCase].number = matchCase



        input_list.append(Entry(searchListBox, width=22, justify = "left", font=('Consolas', 12)))
        input_list[matchCase].config(background = "black", foreground= 'white', font = ('Consolas', 12, 'bold'))


        #input_list[matchCase].bind("<Enter>", on_enter)
        #input_list[matchCase].bind("<Leave>", on_leave)
        #input_list[matchCase].word = matchList[matchCase]
        #input_list[matchCase].number = matchCase

        # checkedButtList.append(IntVar())
        chg_butt.append(HoverButton(searchListBox, text="Change"))
        chg_butt[matchCase].config(background = "black", foreground= 'white', font = ('Consolas', 12, 'bold'), command=lambda c = matchCase: do_something(c))


        searchListBox.window_create("end", window=labelList[matchCase])
        searchListBox.window_create("end", window=std_spacing[matchCase])     
        searchListBox.window_create("end", window=std_list[matchCase])
        searchListBox.window_create("end", window=rmk_spacing[matchCase]) 
        searchListBox.window_create("end", window=remark_list[matchCase]) 
        #searchListBox.window_create("end", window=hoverList[matchCase])

        searchListBox.window_create("end", window=chg_spacing[matchCase])
        searchListBox.window_create("end", window=input_list[matchCase])
        searchListBox.window_create("end", window=chg_butt[matchCase])
        searchListBox.insert("end", "\n")


    
    #highlight_word()

def do_something(c):
    global word_selected
    global remark_selected
    global change_it_to


    # word_selected = matchDf[matchDf['new_werd_order'] == c].word.values()
    

    # word_selected = matchDf.query('new_werd_order==c')['word'].item()


    word_selected = matchDf.loc[matchDf['new_werd_order'] == c, 'word'].item()
    remark_selected = matchDf.loc[matchDf['new_werd_order'] == c, 'remark'].item()
    change_it_to = input_list[c].get()


    # remark_selected = matchDf.query('new_werd_order==line_clicked')['remark'].item()   # alternative way to do it
    # change_it_to = input_list[line_clicked].get()

    print("Current game ID is: {}".format(currentGameId))

    print("Word is: {}".format(word_selected))

    print("Remark is: {}".format(remark_selected))

    print("Input is: {}".format(change_it_to))

    if change_it_to:
        generate_change_code()
    else:
        #messagebox.showerror("Error", "Error message")
        messagebox.showwarning("Warning","No STD_WORD entered!")
        #messagebox.showinfo("Information","Informative message")


def generate_change_code():

    chg_df = pd.DataFrame(columns=['id', 'word', 'remark', 'std_word'])


    chg_list = []
    chg_list.append(currentGameId)
    chg_list.append(word_selected)
    chg_list.append(remark_selected)
    chg_list.append(change_it_to)

    chg_df.loc[0] = chg_list

    chg_df.to_csv('step_6_changes.csv', index=False, mode='a', header=False)



    # with open('changelog.csv', 'a') as outcsv:   
    #     #configure writer to write standard csv file
    #     writer = csv.writer(outcsv, lineterminator='\n')
    #     for item in change_array:
    #         #Write item to outcsv
    #         writer.writerow([item[0], item[1]])    



def on_enter(event):
    global hoverList
    global matchCase
    w = getattr(event.widget, "word", "")[1].lower().replace("_"," ")
    global start_pos
    start_pos = 0
    global end_pos
    end_pos = ''
    global std_list
    global std_spacing
    global labelList
    global rmk_spacing
    global remark_list
    global hoverList
    global chg_spacing

    num_selected = getattr(event.widget, "number", "")

    h_word = w.strip()
    
    start_pos = gameDescTxt.search(h_word, '1.0', stopindex=tk.END)

    if start_pos:
        if end_pos:
            gameDescTxt.tag_remove('highlight', start_pos, end_pos)
        end_pos = '{}+{}c'.format(start_pos, len(h_word))            
        gameDescTxt.tag_add('highlight', start_pos, end_pos)
        gameDescTxt.tag_config('highlight', background='yellow', foreground = "black")

    std_list[num_selected].config(background = "yellow", foreground= 'black', font = ('Consolas', 12, 'bold'))
    std_spacing[num_selected].config(background = "yellow", foreground= 'yellow', font = ('Consolas', 12, 'bold'))
    labelList[num_selected].config(background = "yellow", foreground= 'black', font = ('Consolas', 12, 'bold'))
    rmk_spacing[num_selected].config(background = "yellow", foreground= 'yellow', font = ('Consolas', 12, 'bold'))
    remark_list[num_selected].config(background = "yellow", foreground= 'black', font = ('Consolas', 12, 'bold'))
    hoverList[num_selected].config(background = "yellow", foreground= 'yellow', font = ('Consolas', 12, 'bold'))
    chg_spacing[num_selected].config(background = "yellow", foreground= 'yellow', font = ('Consolas', 12, 'bold'))

def on_leave(event):
    global std_list
    global std_spacing
    global labelList
    global rmk_spacing
    global remark_list
    global hoverList
    global chg_spacing

    num_selected = getattr(event.widget, "number", "")
    std_list[num_selected].config(background = "black", foreground= 'white', font = ('Consolas', 12, 'bold'))
    std_spacing[num_selected].config(background = "black", foreground= 'black', font = ('Consolas', 12, 'bold'))
    labelList[num_selected].config(background = "black", foreground= 'white', font = ('Consolas', 12, 'bold'))
    std_spacing[num_selected].config(background = "black", foreground= 'black', font = ('Consolas', 12, 'bold'))
    rmk_spacing[num_selected].config(background = "black", foreground= 'black', font = ('Consolas', 12, 'bold'))
    remark_list[num_selected].config(background = "black", foreground= 'white', font = ('Consolas', 12, 'bold'))
    hoverList[num_selected].config(background = "black", foreground= 'black', font = ('Consolas', 12, 'bold'))    
    chg_spacing[num_selected].config(background = "black", foreground= 'black', font = ('Consolas', 12, 'bold'))        
    gameDescTxt.tag_remove('highlight', '1.0', tk.END)

def load_file():
    global df
    global currentGameId
    df = pd.read_csv('{}.csv'.format(loadFileInput.get()), index_col ="index")
    #df = pd.read_csv('andrew_100.csv', index_col ="index")
    df = df.astype({"id": int, 
                    "game_num": int, 
                    "word": str, 
                    "game_name": str, 
                    "game_description": str,
                    "stemmed_word": str,
                    "changed_word": str, 
                    "remark": str, 
                    "std_word": str,
                    "occurances": int,
                    "duplicate": int})      
    
    df = df.sort_values(['id', 'std_word'], ascending=[True, False])

    df.reset_index(inplace=True)

    currentGameId = df.iloc[0].id

    update_info()   
    update_std_words()

def filter_std_alpha(letter):
    letter = letter.lower()
    bwList = df['std_word'][df['std_word'] != "nan"].tolist()
    bwList = sorted(set(bwList))
    stdListBox.delete(0, tk.END)

    for item in bwList:
        if item[0] == letter:          
            stdListBox.insert(tk.END, item)     

def update_std_words():
    stdListBox.delete(0, tk.END)
    bwList = df['std_word'][df['std_word'] != "nan"].tolist()
    filterTerm = stdSearchInput.get()
    if filterTerm == "":
        for item in sorted(list(set(bwList))):
            stdListBox.insert(tk.END, item)   
    else:
        for item in sorted(list(set(bwList))):
            if filterTerm in item:
                stdListBox.insert(tk.END, item)     

def std_search():
    global filterTerm
    filterTerm = stdSearchInput.get()
    update_std_words()

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
rootWidth = 1900
rootHeight = 1000
root.geometry('{}x{}+10+40'.format(rootWidth, rootHeight))
root.resizable(width=False, height=False)

# SET FRAME DIMENSIONS
frame1 = Frame(root, width=700, height=1000)
frame1.place(x=0,y=0)
frame1.config(bg="grey11")
frame2 = Frame(root, width=1200, height=1000)
frame2.place(x=700,y=0)
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
prevBtn.place(x=10,y=70)
nextBtn = HoverButton(frame1, text="Next", command=next_row, padx=2, pady=2)
nextBtn.place(x=100,y=70)



jumpToBtn = HoverButton(frame1, text="Jump", command=jump_to_index)
jumpToBtn.place(x=210,y=70)
jumpToInput = Entry(frame1, width=42, justify = "left", font=('Consolas', 12))
jumpToInput.place(x=275,y=74)
jumpToInput.configure(background = "black", foreground="white", font=('Consolas', 12))

gameDescTxt = st.ScrolledText(frame1, undo=True, width=38, height=45, wrap="word", bg = "black", fg = "white", font=('Consolas', 12))
gameDescTxt.place(x=325, y=120)
gameDescTxt.insert(1.0, "LOAD A FILE..")


stdSearchBtn = HoverButton(frame1, text="Search", command=std_search, padx=2, pady=2)
stdSearchInput = Entry(frame1, width=20, justify = "left", font=('Consolas', 12))
stdSearchBtn.place(x=10, y=105)
stdSearchInput.place(x=95, y=109)


buttons = []
xcoord = 0
ycoord = 150
letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
           "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",]

for i in range(26):
    xcoord +=20
    b = HoverButton(frame1, width = 2, height=1, padx=0, pady=0, text = "%s" % (letters[i]), command=lambda i=i: filter_std_alpha(letters[i]))
    if i <= 12:
        b.place(x=xcoord, y=ycoord)
    else:
        b.place(x=xcoord-260, y=ycoord+25)
    buttons.append(b)

stdCanvas = Canvas(frame1, bg='green', width=340, height=900)
stdCanvas.place(x=10,y=210)

stdScrollbar = Scrollbar(stdCanvas, orient="vertical")
stdScrollbar.pack(side="right", fill="y")
stdListBox = Listbox(stdCanvas, width=40, height=48, background = "black", foreground="white", font = ('Consolas', 10, 'bold'))
stdListBox.pack()
stdListBox.insert(tk.END, "LIST OF STANDARDIZED WORDS..")
stdListBox.configure(yscrollcommand=stdScrollbar.set)
stdScrollbar.config(command=stdListBox.yview)


#FRAME 2


loadFileBtn = HoverButton(frame2, text="Load", command=load_file)
loadFileBtn.place(x=710,y=955)
loadFileInput = Entry(frame2, width=42, justify = "left", font=('Consolas', 12))
loadFileInput.place(x=775,y=959)
loadFileInput.configure(background = "black", foreground="white", font=('Consolas', 12))


word_label = Label(frame2, text="WORD")
word_label.place(x=5,y=5)
word_label.configure(background = "black", foreground="white", font=('Consolas', 12))

std_label = Label(frame2, text="STD WORD")
std_label.place(x=300,y=5)
std_label.configure(background = "black", foreground="white", font=('Consolas', 12))

rmk_label = Label(frame2, text="REMARK")
rmk_label.place(x=600,y=5)
rmk_label.configure(background = "black", foreground="white", font=('Consolas', 12))

new_std_label = Label(frame2, text="NEW STD_WORD:")
new_std_label.place(x=825,y=5)
new_std_label.configure(background = "black", foreground="white", font=('Consolas', 12))


searchCanvas = Canvas(frame2, bg='black', width=350, height=900)
searchCanvas.place(x=5,y=60)
searchListBox = st.ScrolledText(searchCanvas, width=140, height=52, wrap="none")
searchListBox.configure(background = "black")
searchListBox.pack() 

# backMatchCanvas = Canvas(frame2, bg='black', width=800, height=900)
# backMatchCanvas.place(x=350,y=5)
# backMatchBox = st.ScrolledText(backMatchCanvas, width=120, height=46, wrap="none")
# backMatchBox.configure(background = "black", foreground="white", font=('Consolas', 12))
# backMatchBox.place(x=5,y=5)

# MAIN LOOP
root.mainloop()