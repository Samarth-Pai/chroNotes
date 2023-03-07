# Author : Samarth Pai
# Program : chroNotes - A simple text editor
from os import path
from tkinter import (
    Frame,
    Text,
    Menu,
    Tk,
    BOTH,
    Scrollbar,
    filedialog,
    messagebox,
    ttk,
    Listbox,
    font,
    END,
)
import string

root = Tk()
root.geometry("700x388")
root.title("chroNotes")
file = None

# Test area
textArea = Text(
    root, font="Jetbrains\ mono 13", undo=1, maxundo=-1, autoseparators=True
)
textArea.pack(expand=1, fill=BOTH, side="left")

# ScrollBar setting
scroll = Scrollbar(textArea, command=textArea.yview)
scroll.pack(side="right", fill="y")
textArea.config(yscrollcommand=scroll.set)

# Subroutine
def newFile():
    file = None
    root.title("chroNotes")
    textArea.delete("1.0", "end")


def openFile():
    file = filedialog.askopenfile(
        defaultextension=".txt",
        filetypes=[("All files", ".*"), ("Text document", ".txt")],
    )
    if file != None:
        textArea.delete("1.0", "end")
        textArea.insert("1.0", file.read())
        root.title(file.name + " - chroNotes")


def saveFile():
    global file
    print(file)
    if file == None:
        file = filedialog.asksaveasfile(
            initialfile="Untitled.txt", defaultextension=".txt"
        )
        if file != None:
            with open(file.name, "w") as f:
                f.write(textArea.get("1.0", "end"))
            root.title(file.name + " - chroNotes")

    else:
        with open(file.name, "w") as f:
            f.write(textArea.get("1.0", "end"))


def saveAsFile():
    global file
    savedFile = filedialog.asksaveasfile(
        initialfile="Untitled.txt", defaultextension=".txt"
    )
    if savedFile != None:
        file = savedFile
        with open(savedFile.name, "w") as f:
            f.write(textArea.get("1.0", "end"))
        root.title(savedFile.name + " - chroNotes")


def closeApp():
    global file
    print(file)
    saveOrNot = messagebox.askyesno(
        "File", "Do you want to save your current changes in the file?"
    )
    print(saveOrNot)
    if saveOrNot:
        saveFile()
    else:
        root.quit()


def fontSizeChange(x):
    global file
    fontt = textArea["font"].split(" ")
    fontt[-1] = str(x)
    textArea["font"] = " ".join(fontt)


def fontStyleChange():
    global file, fontBox
    fontWindow = Tk()
    fontWindow.geometry("418x400")
    fontWindow.resizable(0, 0)
    fontWindow.title("Font selection")

    fontBox = Listbox(fontWindow, width=50)
    fontBox.pack(side="left", fill=BOTH)

    families = font.families()
    for family in families:
        fontBox.insert(END, family)

    def fontStyleApply(x):
        stile = textArea["font"].split(" ")
        fontStr = str()
        for search in stile:
            if search.isdigit():
                fontStr += search
        textArea["font"] = fontBox.selection_get().replace(" ", "\ ") + " " + fontStr

    fontWindow.bind("<Button-1>", fontStyleApply)

    familyScrollbar = Scrollbar(fontWindow, command=fontBox.yview, orient="vertical")
    familyScrollbar.pack(side="right", fill=BOTH)
    fontBox.config(yscrollcommand=familyScrollbar.set)

    fontWindow.mainloop()


# MenuBar lafda
mainMenu = Menu(root, tearoff=0)
root.configure(menu=mainMenu)

fileMenu = Menu(mainMenu, tearoff=0)
fileMenu.add_command(label="New", command=newFile)
fileMenu.add_command(label="Open", command=openFile)
fileMenu.add_command(label="Save", command=saveFile)
fileMenu.add_command(label="Save as", command=saveAsFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=closeApp)
mainMenu.add_cascade(label="File", menu=fileMenu)

editMenu = Menu(mainMenu, tearoff=0)
editMenu.add_command(label="Copy", command=lambda: textArea.event_generate("<<Copy>>"))
editMenu.add_command(label="Cut", command=lambda: textArea.event_generate("<<Cut>>"))
editMenu.add_command(
    label="Paste", command=lambda: textArea.event_generate("<<Paste>>")
)
editMenu.add_separator()
editMenu.add_command(label="Undo", command=textArea.edit_undo)
editMenu.add_command(label="Redo", command=textArea.edit_redo)
mainMenu.add_cascade(label="Edit", menu=editMenu)


viewMenu = Menu(mainMenu, tearoff=0)
fontMenu = Menu(viewMenu, tearoff=0)

fontSizeMenu = Menu(fontMenu, tearoff=0)
for i in range(7, 41):
    fontSizeMenu.add_command(label=str(i), command=lambda x=i: fontSizeChange(x))


fontStyleMenu = Menu(fontMenu, tearoff=0)
for i in font.families():
    fontStyleMenu.add_command(
        label=i, command=lambda x=i: fontStyleChange(x), font=i.replace(" ", "\ ")
    )

fontMenu.add_command(label="Font style", command=fontStyleChange)
fontMenu.add_cascade(label="Font size", menu=fontSizeMenu)
viewMenu.add_cascade(label="Font", menu=fontMenu)
mainMenu.add_cascade(label="View", menu=viewMenu)


helpMenu = Menu(mainMenu, tearoff=0)
helpMenu.add_command(
    label="About chroNotes",
    command=lambda: messagebox.showinfo(
        "About chroNotes",
        "chroNotes version 1.0\nThis is a simple text editor progam made by Samarth Pai ",
    ),
)
mainMenu.add_cascade(label="Help", menu=helpMenu)

root.bind("Control-S",saveFile)

# On closing the window
root.protocol("WM_DELETE_WINDOW", closeApp)
root.mainloop()
