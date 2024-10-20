#Imports
from tkinter import Tk, mainloop, IntVar, messagebox
from tkinter.ttk import *
from random import randint

#Window Setup
root = Tk()
root.geometry("550x600+50+50")
root.title("2048")
root.config(bg="#faf8f0")
root.resizable(False, False)

#Stylesheet
css = Style(root)
css.configure("Game.TFrame", background="#9c8b7c")
css.configure("Head.TFrame", background="#faf8f0")
css.configure("Score.TLabel", foreground="#9c8b7c", font=("Consolas", 18, "bold"), background="#faf8f0")
css.configure("High.TLabel", foreground="#ffd700", font=("Consolas", 18, "bold"), background="#faf8f0")
css.configure("HeadButton.TButton", foreground="#9c8b7c", font=("Consolas", 14, "bold"), background="#faf8f0", width=2, bordercolor="#9c8b7c")
css.configure("Empty.TLabel", background="#bdac97")
css.configure("Block.TLabel", font=("Helvetica", 30, "bold"))

#Globals
speed = 0.05
scoreVar = IntVar(value=0)
highVar = IntVar(value=0)
colors = [None, "#eee4da", "#ebd8b6", "#f2b177", "#f69462", "#f78064", "#f76543", "#f1d26d", "#f2d366", "#edc651", "#eec744", "#ecc230", "#fe3d3e"]

#Functions
def possible(*args):
    from random import choice
    array = []
    for object, count in zip(args[::2], args[1::2]): array += [object]*count
    return choice(array)
def start():
    Block().place()
    Block().place()
    startButton["state"] = "disabled"
    restartButton["state"] = "enabled"
def restart():
    for cell in grid:
        if cell: cell.destroy()
    startButton["state"] = "enabled"
    restartButton["state"] = "disabled"
    highVar.set(max(highVar.get(), scoreVar.get()))
    scoreVar.set(0)
def increaseScore(increament):
    scoreVar.set(scoreVar.get()+increament)

#Header
header = Frame(root, width=500, height=50, style="Head.TFrame")
header.pack_propagate(False)
header.pack(padx=12.5, pady=12.5)

highLabel = Label(header, textvariable=highVar, style="High.TLabel")
highLabel.pack(side="left", expand=True)

scoreLabel = Label(header, textvariable=scoreVar, style="Score.TLabel")
scoreLabel.pack(side="left", expand=True)

restartButton = Button(header, text="⨉", command=restart, style="HeadButton.TButton")
restartButton.pack(side="right")
restartButton["state"] = "disabled"

startButton = Button(header, text="▶", command=start, style="HeadButton.TButton")
startButton.pack(side="right")


#Game Frame
game = Frame(root, width=500, height=500, style="Game.TFrame")
game.pack_propagate(False)
game.pack()
for x in range(0, 100, 25):
    for y in range(0, 100, 25):
        Label(game, style="Empty.TLabel").place(relx=(x+12.5)/100, rely=(y+12.5)/100, relheight=0.216, relwidth=0.216, anchor="center")

#Matrix & Grid
matrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
grid = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]


#Block Object 
class Block:

    def __init__(self) -> None:
        if matrix.count(0) == 0:
            del self
            return "Filled"
        self.pos = randint(0, 15)
        while matrix[self.pos] != 0: self.pos = randint(0, 15)
        self.x = ((self.pos%4)*0.25)+0.125
        self.y = ((self.pos//4)*0.25)+0.125
        self.power = possible(1, 6, 2, 1)
        self.var = IntVar(value=2**self.power)
        self.block = Label(game, textvariable=self.var, background=colors[self.power], foreground="#ffffff" if self.power > 2 else "#756452", style="Block.TLabel", justify="center", anchor="center")

    def place(self) -> None:
        self.block.place(relx=self.x, rely=self.y, relwidth=0.216, relheight=0.216, anchor="center")
        matrix[self.pos] = self.power
        grid[self.pos] = self

    def destroy(self) -> None:
        self.block.destroy()
        grid[self.pos] = None
        matrix[self.pos] = 0
        del self

    def set(self) -> None:
        self.var.set(2**self.power)
        self.block.config(background=colors[self.power])
        grid[self.pos] = self
        matrix[self.pos] = self.power

    def slide(self, newPos: int) -> None:
        self.x = ((newPos%4)*0.25)+0.125
        self.y = ((newPos//4)*0.25)+0.125
        self.block.place(relx=self.x, rely=self.y, anchor="center")
                    
    def merge(self, direction: str, mixed: bool= False) -> None:
        global movement
        if direction == "Left":
            if self.pos%4 == 0: return
            cell = grid[self.pos-1]
            if cell == None:
                self.slide(self.pos-1)
                grid[self.pos] = None
                matrix[self.pos] = 0
                grid[self.pos-1] = self
                matrix[self.pos-1] = self.power
                self.pos -= 1
                self.merge("Left")
                movement = True
            elif cell.power == self.power and not mixed:
                grid[self.pos] = None
                matrix[self.pos] = 0
                self.slide(self.pos-1)
                increaseScore(2**(cell.power+1))
                self.destroy()
                cell.power += 1
                cell.set()
                cell.merge("Left", True)
                movement = True
        if direction == "Right":
            if self.pos%4 == 3: return
            cell = grid[self.pos+1]
            if cell == None:
                self.slide(self.pos+1)
                grid[self.pos] = None
                matrix[self.pos] = 0
                grid[self.pos+1] = self
                matrix[self.pos+1] = self.power
                self.pos += 1
                self.merge("Right")
                movement = True
            elif cell.power == self.power and not mixed:
                grid[self.pos] = None
                matrix[self.pos] = 0
                self.slide(self.pos+1)
                increaseScore(2**(cell.power+1))
                self.destroy()
                cell.power += 1
                cell.set()
                cell.merge("Right", True)
                movement = True
        if direction == "Up":
            if self.pos//4 == 0: return
            cell = grid[self.pos-4]
            if cell == None:
                self.slide(self.pos-4)
                grid[self.pos] = None
                matrix[self.pos] = 0
                grid[self.pos-4] = self
                matrix[self.pos-4] = self.power
                self.pos -= 4
                self.merge("Up")
                movement = True
            elif cell.power == self.power and not mixed:
                grid[self.pos] = None
                matrix[self.pos] = 0
                self.slide(self.pos-4)
                increaseScore(2**(cell.power+1))
                self.destroy()
                cell.power += 1
                cell.set()
                cell.merge("Up", True)
                movement = True
        if direction == "Down":
            if self.pos//4 == 3: return
            cell = grid[self.pos+4]
            if cell == None:
                self.slide(self.pos+4)
                grid[self.pos] = None
                matrix[self.pos] = 0
                grid[self.pos+4] = self
                matrix[self.pos+4] = self.power
                self.pos += 4
                self.merge("Down")
                movement = True
            elif cell.power == self.power and not mixed:
                grid[self.pos] = None
                matrix[self.pos] = 0
                self.slide(self.pos+4)
                increaseScore(2**(cell.power+1))
                self.destroy()
                cell.power += 1
                cell.set()
                cell.merge("Down", True)
                movement = True

#Key Events
def keyPress(key):
    global movement
    movement = False
    if key == "Left":
        for cell in grid:
            if cell != None:
                cell.merge("Left")
    if key == "Right":
        for cell in grid[::-1]:
            if cell != None:
                cell.merge("Right")
    if key == "Up":
        tempGrid = grid[::4]+grid[1::4]+grid[2::4]+grid[3::4]
        for cell in tempGrid:
            if cell != None:
                cell.merge("Up")
    if key == "Down":
        tempGrid = grid[::4][::-1]+grid[1::4][::-1]+grid[2::4][::-1]+grid[3::4][::-1]
        for cell in tempGrid:
            if cell != None:
                cell.merge("Down")
    if movement:
        Block().place()
    if matrix.count(0) == 0:
        matching = False
        for cell in grid:
            if cell.pos%4 != 0:
                if grid[cell.pos-1].power == cell.power:
                    matching = True
            if cell.pos%4 != 3:
                if grid[cell.pos+1].power == cell.power:
                    matching = True
            if cell.pos//4 != 0:
                if grid[cell.pos-4].power == cell.power:
                    matching = True
            if cell.pos//4 != 3:
                if grid[cell.pos+4].power == cell.power:
                    matching = True
        if not matching:
            messagebox.showinfo("Game Over", "You have no possible moves left")
            restart()

root.bind("<Right>", lambda _: keyPress("Right"))
root.bind("<Left>", lambda _: keyPress("Left"))
root.bind("<Down>", lambda _: keyPress("Down"))
root.bind("<Up>", lambda _: keyPress("Up"))

#Mainloop
mainloop()