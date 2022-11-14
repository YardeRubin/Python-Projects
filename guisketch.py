import typing

import game
from game import *
import tkinter as tk
from boggle_board_randomizer import *


class Transition_Root:
    def _init_(self):
        pass

    def run_transition_root(self):
        print("sss")
        return 6


class Boggle_Gui:
    def _init_(self, game: Game, transition_root: Transition_Root):
        self.game = game
        self.transition_root = transition_root

    def run_game(self):
        self.root = tk.Tk()
        self.board_frame = tk.Frame(self.root)
        self.word_frame = tk.Frame(self.root)
        self.score = tk.Frame(self.root)
        self.timer = tk.Frame(self.root)
        self.words_frame = tk.Frame(self.root)
        self.submit_undo_frame = tk.Frame(self.root, padx=50, pady=100)
        self.init_board_frame()
        self.init_submit_undo_frame()
        self.init_words_list()

    def init_board_frame(self):
        b = self.game.board
        for row_idx, row in enumerate(b):
            for col_idx, letter in enumerate(b[row_idx]):
                self.create_button(row_idx, col_idx, letter)
        self.board_frame.pack()

    def init_submit_undo_frame(self):
        submit_button = tk.Button(self.submit_undo_frame, text="SUBMIT",
                                  command=self.new_word, padx=20, pady=20)
        undo_button = tk.Button(self.submit_undo_frame, text="UNDO",
                                command=self.game.clear_word, padx=20, pady=20)
        submit_button.pack(side=tk.LEFT)
        undo_button.pack(side=tk.RIGHT)
        self.submit_undo_frame.pack(side=tk.BOTTOM)

    def init_words_list(self):
        self.used_words_label = tk.Label(self.words_frame,
                                         text=self.game.found_words)
        self.used_words_label.pack(side=tk.TOP)
        self.words_frame.pack()

    def create_button(self, row_idx, col_idx, letter):
        button = tk.Button(self.board_frame, text=letter, bg="white",
                           fg="black", command=lambda: self.game.add_letter(
                (row_idx, col_idx)))
        button.grid(row=row_idx, column=col_idx)

    def _score(self):
        self.score_label = tk.Label(self.score, text=self.game.score)
        self.pack(side=tk.RIGHT)

    def new_word(self):
        self.game.add_word()
        print("sss")
        self.used_words_label.configure(text=self.game.found_words)
        self.used_words_label.pack(side=tk.TOP)
        self.score_label.configure(text=self.game.score)
        self.pack(side=tk.RIGHT)
        self.words_frame.pack()

    def timer(self):
        self.game.decrease_time()
        if self.game.time_over():
            self.finish_game()
        self.root.after(1000, self.timer())

    def finish_game(self):
        # self.transition_root.run_transition_root()
        self.root.destroy()