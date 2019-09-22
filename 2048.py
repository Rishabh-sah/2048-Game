from tkinter import *
import random
import numpy
FONT = ("Verdana", 40, "bold")
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                         16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                         128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                         1024: "#edc53f", 2048: "#edc22e",

                         4096: "#eee4da", 8192: "#edc22e", 16384: "#f2b179",
                         32768: "#f59563", 65536: "#f67c5f", }
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2",
                   256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2",
                   2048: "#f9f6f2",

                   4096: "#776e65", 8192: "#f9f6f2", 16384: "#776e65",
                   32768: "#776e65", 65536: "#f9f6f2", }
class vital(Frame):
    def __init__(self):
        KEY_UP = "'w'"
        KEY_DOWN = "'s'"
        KEY_LEFT = "'a'"
        KEY_RIGHT = "'d'"
        Frame.__init__(self)
        self.grid()
        self.master.title('2048 - GAME')
        self.master.iconbitmap(r'2048.ico')
        self.master.bind("<Key>", self.key_down)
        self.commands = {KEY_UP: self.up, KEY_DOWN: self.down,
                         KEY_LEFT: self.left, KEY_RIGHT: self.right}
        self.grid_cells = []
        background = Frame(self, bg="#92877d")
        self.init_grid(background)
        self.buttons(background)
        self.init_matrix()
        self.update_grid_cells()
        self.mainloop()
    def game_state(self,m):
        for i in range(4):
            for j in range(3):
                if m[i][j + 1] == m[i][j]:
                    return "not over"
        for i in range(3):
            for j in range(4):
                if m[i+1][j] == m[i][j]:
                    return "not over"
        for i in range(4):
            for j in range(4):
                if m[i][j] == 0:
                    return 'not over'
        return 'lose'
    def init_grid(self,background):
        background.grid()
        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = Frame(background, bg="#9e948a",width=100,height=100)
                cell.grid(row=i, column=j, padx=10,pady=10)
                t = Label(master=cell, text="",
                          bg="#9e948a",
                          justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)
    def init_matrix(self):
        self.matrix = self.new_game(4)
        self.history_matrixs = list()
        self.matrix = self.add_two(self.matrix)
        self.matrix = self.add_two(self.matrix)
    def update_grid_cells(self):
        self.history_matrixs.append(self.matrix)
        for i in range(4):
            for j in range(4):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg="#9e948a")
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                        fg=CELL_COLOR_DICT[new_number])
        if self.game_state(self.matrix) == 'lose':
            for i in range(4):
                for j in range(4):
                    self.grid_cells[i][j].configure(
                        text="LOST", bg="#9e948a")
    def add_two(self,mat):
        a = random.randint(0, 3)
        b = random.randint(0, 3)
        while (mat[a][b] != 0):
            a = random.randint(0, 3)
            b = random.randint(0, 3)
        mat[a][b] = 2
        return mat
    def buttons(self, background, right=None):
        self.button1 = Button(background, text="UP", width=20)
        self.button1.bind("<Button-1>", self.up)
        self.button1.grid(row=6,column=1)
        self.button2 = Button(background, text="LEFT", width=20)
        self.button2.bind("<Button-1>", self.left)
        self.button2.grid(row=7,column=0,sticky="e")
        self.button3 = Button(background, text="DOWN", width=20)
        self.button3.bind("<Button-1>", self.down)
        self.button3.grid(row=7,column=1)
        self.button4 = Button(background, text="RIGHT", width=20)
        self.button4.bind("<Button-1>", self.right)
        self.button4.grid(row=7,column=2,sticky="w")
        self.button5 = Button(background, text="NEW GAME", width=8)
        self.button5.bind("<Button-1>", self.newgame)
        self.button5.grid(row=7, column=3, sticky="w")
    def key_down(self, event):
        if self.game_state(self.matrix) == 'lose':
            pass
        else:
            key = repr(event.char)
            if key in self.commands:
                done = self.commands[key](self.matrix)
                if done:
                    self.matrix = self.add_two(self.matrix)
                    self.history_matrixs.append(self.matrix)
                    self.update_grid_cells()
    def new_game(self,n):
        matrix = []
        for i in range(4):
            matrix.append([0] * 4)
        return matrix
    def gen(self):
        return random.randint(0, 3)
    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2
    def moveup(self,done):
        for i in range(0,3):
            for j in range(0,4):
                if self.matrix[i][j]==0 and self.matrix[i+1][j]!=0:
                    self.matrix[i][j] = self.matrix[i + 1][j]
                    self.matrix[i + 1][j] = 0
                    done = True
        return done
    def moveleft(self,done):
        for j in range(0,3):
            for i in range(0,4):
                if self.matrix[i][j]==0 and self.matrix[i][j+1]!=0:
                    self.matrix[i][j] = self.matrix[i][j+1]
                    self.matrix[i][j+1] = 0
                    done = True
        return done
    def moveright(self,done):
        for j in range(3,0,-1):
            for i in range(0,4):
                if self.matrix[i][j]==0 and self.matrix[i][j-1]!=0:
                    self.matrix[i][j] = self.matrix[i][j-1]
                    self.matrix[i][j-1] = 0
                    done = True
        return done
    def movedown(self,done):
        for i in range(3,0,-1):
            for j in range(0,4):
                if self.matrix[i][j]==0 and self.matrix[i-1][j]!=0:
                    self.matrix[i][j] = self.matrix[i-1][j]
                    self.matrix[i-1][j] = 0
                    done = True
        return done
    def up(self,event):
        done = False
        done = self.moveup(done)
        done = self.moveup(done)
        for i in range(0, 3, 1):
            for j in range(0, 4, 1):
                if self.matrix[i][j] == self.matrix[i + 1][j] and self.matrix[i][j] != 0:
                    self.matrix[i][j] *= 2
                    self.matrix[i + 1][j] = 0
                    done = True
        done = self.moveup(done)
        done = self.moveup(done)
        if done:
            self.generate_next()
        self.update_grid_cells()
    def down(self,event):
        done = False
        done = self.movedown(done)
        done = self.movedown(done)
        for i in range(3, -1, -1):
            for j in range(3, -1, -1):
                if self.matrix[i][j] == self.matrix[i - 1][j] and self.matrix[i][j] != 0:
                    self.matrix[i][j] *= 2
                    self.matrix[i - 1][j] = 0
                    done = True
        done = self.movedown(done)
        done = self.movedown(done)
        if done:
            self.generate_next()
        self.update_grid_cells()
    def right(self,event):
        done = False
        done = self.moveright(done)
        done = self.moveright(done)
        for i in range(3, -1, -1):
            for j in range(3, 0, -1):
                if self.matrix[i][j] == self.matrix[i][j - 1] and self.matrix[i][j] != 0:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j - 1] = 0
                    done = True
        done = self.moveright(done)
        done = self.moveright(done)
        if done:
            self.generate_next()
        self.update_grid_cells()
    def left(self,event):
        done = False
        done = self.moveleft(done)
        done = self.moveleft(done)
        for i in range(0, 4, 1):
            for j in range(0, 3, 1):
                if self.matrix[i][j] == self.matrix[i][j + 1] and self.matrix[i][j] != 0:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    done = True
        done = self.moveleft(done)
        done = self.moveleft(done)
        if done:
            self.generate_next()
        self.update_grid_cells()
    def newgame(self,event):
        self.init_matrix()
        self.update_grid_cells()
gamegrid=vital()