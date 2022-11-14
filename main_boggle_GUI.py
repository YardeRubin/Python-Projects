import typing
import boggle_board_randomizer
from quit_menu_GUI import *
from game import *
import tkinter as tk
from boggle_board_randomizer import *
import tkinter.font as font


LIST_OF_WORDS = []
with open("boggle_dict.txt","r") as file:
    for line in file:
        LIST_OF_WORDS.append(file.readline()[:-1])

#global shit:
TIMER = 6
MAIN_GUI_BACKGROUND = "war_image.png"
MAIN_GUI_SIZE =  "1024x576"
WIDTH_MAIN =1024
HEIGHT_MAIN = 576


#Transition_Root Global Shit:
TRANSITION_ROOT_GEOMETRY = "768x439"
PLAY_AGAIN_IMAGE = "biden_zelensky.png"
WIDTH_TRASNITION_ROOT = 768
HEIGHT_TRASNITION_ROOT = 439

################################################################################
class Transition_Root:
    """
    a class that creates the GUI  for the play again window
    """
    def play_again_window(self,score):
        self.play_again_root = tk.Tk()
        self.play_again_root.title("PLAY AGAIN?")
        self.play_again_root.resizable(False, False)
        self.play_again_root.geometry(TRANSITION_ROOT_GEOMETRY)
        # get an i  mage:
        play_again_image = tk.PhotoImage(file=PLAY_AGAIN_IMAGE)

        # set canvas and background:
        play_again_canvas = tk.Canvas(self.play_again_root, width=WIDTH_TRASNITION_ROOT,
                                      height=HEIGHT_TRASNITION_ROOT)
        play_again_canvas.pack(fill="both", expand=True)
        play_again_canvas.create_image(0, 0, image=play_again_image,
                                       anchor="nw")

        # add text:
        play_again_canvas.create_text(370, 30, text="SOLDIER!",
                                      font=("David", 20), fill="red")
        play_again_canvas.create_text(370, 55,
                                      text="DO YOU WANT TO PLAY AGAIN?",
                                      font=("David", 20), fill="red")
        play_again_canvas.create_text(370, 75, text="YOUR SCORE IS: "+str(score))
        # create buttons:
        play_again_button = tk.Button(self.play_again_root, text="PLAY AGAIN",
                                      padx=20, pady=20, command=self.play_gagin_function)
        quit_button = tk.Button(self.play_again_root, text="QUIT",
                                command=exit, padx=20, pady=20)
        # place buttons:
        play_again_canvas.create_window(300, 370, anchor="nw",
                                        window=play_again_button)
        play_again_canvas.create_window(400, 370, anchor="nw",
                                        window=quit_button)
        self.play_again_root.mainloop()


    def play_gagin_function(self):
        self.play_again_root.destroy()
        new_board = boggle_board_randomizer.randomize_board()
        new_game = Game(new_board,LIST_OF_WORDS,TIMER)
        new_gui = Boggle_Gui(new_game)
        new_gui.run_game()


################################################################################
class Boggle_Gui:
    """
    a class that creates the GUI for the proccess of the game
    """
    def __init__(self, game: Game):
        self.game = game
        #transition root object:
        self.transition_root = Transition_Root()
        #quit menu object:
        self.quit_menu = QUIT_MENU()


    def run_game(self):
        self.letters_dict = dict()
        self.root = tk.Tk()
        self.root.geometry(MAIN_GUI_SIZE)
        self.root.resizable(False,False)

        # get an image:
        self.image = tk.PhotoImage(file=MAIN_GUI_BACKGROUND)

        #cerate canvas:
        self.canvas = tk.Canvas(self.root, width=WIDTH_MAIN, height=HEIGHT_MAIN)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0,0, image=self.image, anchor="nw")

        #create frames:
        self.board_frame = tk.Frame(self.root)
        self.current_word_frame = tk.Frame(self.root)
        self.score_frame = tk.Frame(self.root)
        self.timer_frame = tk.Frame(self.root)
        self.words_list_frame = tk.Frame(self.root)
        self.submit_undo_frame = tk.Frame(self.root)

        #create quit_button:
        self.myFont = font.Font(family='Helvetica', size=10, weight='bold')
        quit_button = tk.Button(self.root,text="QUIT", padx=20, pady=20, command=self.quit_menu.quitter_menu, bg="red", fg="white")
        quit_button["font"]=self.myFont
        self.canvas.create_window(30,30,window=quit_button)

        #init frames:
        self.init_board_frame()
        self.init_current_word_frame()
        self.init_submit_undo_frame()
        self.init_words_list_frame()
        self.init_score_frame()
        self.init_timer_frame()

        #strat timer:
        self.root.after(1000, self.timer)

        #run loop:
        self.root.mainloop()

    #INIT FUNCTIOS:
    def init_board_frame(self):
        """
        a method that create the grid buttons with the "create_button" function
        also place the grid frame on the canvas
        :return: None
        """
        board = self.game.board
        for row_idx, row in enumerate(board):
            for col_idx, letter in enumerate(board[row_idx]):
                 self.letters_dict[(row_idx,col_idx)] = self.create_button(row_idx, col_idx, letter)

        # create_window:
        self.canvas.create_window(850,400,window=self.board_frame)

    def init_score_frame(self):
        self.score_label = tk.Label(self.score_frame, text=self.game.score,pady=20,padx=20)
        self.score_label.pack(side=tk.RIGHT)
        self.canvas.create_window(850,80,window=self.score_frame)

    def init_submit_undo_frame(self):
        submit_button = tk.Button(self.submit_undo_frame, text="SUBMIT",
                                  command=self.new_word , padx=20, pady=20)
        undo_button = tk.Button(self.submit_undo_frame, text="CLEAR",
                                command=self.del_word, padx=20, pady=20)
        submit_button["font"] = self.myFont
        undo_button["font"] =self.myFont
        submit_button.pack(side=tk.LEFT)
        undo_button.pack(side=tk.RIGHT)
        self.canvas.create_window(850,187,window=self.submit_undo_frame)

    def init_current_word_frame(self):
        self.current_word_label = tk.Label(self.current_word_frame, text = self.game.current_word)
        self.current_word_label.pack()
        self.canvas.create_window(850,240,window=self.current_word_frame)

    def init_words_list_frame(self):
        self.down_row = ""
        self.used_words_label = tk.Label(self.words_list_frame, text=self.down_row)
        self.used_words_label.pack(side=tk.TOP)

    def init_timer_frame(self):
        mins, secs = divmod(self.game.timer, 60)
        self.timer_label = tk.Label(self.timer_frame,
                                    text=str(mins) + " : " + str(secs),padx=20,pady=20, fg="white", bg = "black")
        self.timer_label.pack()
        self.canvas.create_window(994, 30, window=self.timer_frame)


    #create buttons for grid:

    def create_button(self, row_idx, col_idx, letter):
        """
        method that creates button and set their colur, size, font.
        :param row_idx: in the board
        :param col_idx: in the board
        :param letter: the letter the coordinate represent
        :return: button
        """

        button = tk.Button(self.board_frame, text=letter, bg="#0052cc",
                           fg="#ffffff",
                           command=lambda: self.new_letter(row_idx, col_idx),
                           height=3, width=5)
        button['font'] = self.myFont
        button.grid(row=row_idx, column=col_idx)
        return button

    #functions that disable the buttons grid:

    def disable_other_letters(self,row_idx,col_idx):
        self.able_disable_all_letters("disable")
        for coordinate in nearby((row_idx,col_idx)):
            if validated_coordinate(coordinate, self.game.board,self.game.current_path):
                self.letters_dict[coordinate]["state"]= "normal"

    def able_disable_all_letters(self,state):
        for row in range(len(self.game.board)):
            for col in range(len(self.game.board[row])):
                self.letters_dict[(row,col)]["state"]= state


    #updating functions:

    def new_letter(self, row_idx, col_idx):
        self.disable_other_letters(row_idx, col_idx)
        self.game.add_letter((row_idx, col_idx))
        self.current_word_label.configure(text = self.game.current_word)

    def del_word(self):
        self.game.clear_word()
        self.current_word_label.configure(text = self.game.current_word)
        self.able_disable_all_letters("normal")

    def new_word(self):
        self.game.add_word()
        self.down_row = ""
        for i in range(len(self.game.found_words)):
            if i % 7 == 0 and i != 0:
                self.down_row += self.game.found_words[i] + "\n"
            else:
                self.down_row += self.game.found_words[i]+", "
        self.used_words_label.configure(text = self.down_row)
        self.used_words_label.pack(side=tk.TOP)
        self.score_label.configure(text=self.game.score)
        self.score_label.pack(side=tk.RIGHT)
        self.canvas.create_window(150,400,window=self.words_list_frame)
        self.able_disable_all_letters("normal")

    #timer function:

    def timer(self):
        self.game.decrease_time()
        mins, secs = divmod(self.game.timer, 60)
        self.timer_label.configure(text=str(mins) + " : " + str(secs))
        if self.game.time_over():
            self.finish_game()
            self.transition_root.play_again_window(self.game.score)
        self.root.after(1000, self.timer)


    def finish_game(self):
        self.root.destroy()


