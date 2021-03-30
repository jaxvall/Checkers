from tkinter import *
from itertools import product
from Checkers import *


class Menu(Frame):
    '''Class for creating the menu.'''

    def __init__(self):
        Frame.__init__(self)
        self.menuFrame = Frame(width=240, height=80)
        self.menuFrame.pack(expand=1, fill=BOTH, side=TOP)
        self.menuFrame.pack_propagate(0)
        self.button1 = Button(self.menuFrame, text="Play!", font=("Helvetica", "10", "bold"), width=13, height=2,
                              command=board.start_game, cursor="heart", relief=RIDGE,)
        self.button1.pack()
        self.button2 = Button(self.menuFrame, text="Settings", font=("Helvetica", "10", "bold"), width=13, height=2,
                              command=board.show_settings, relief=RIDGE,)
        self.button2.pack()
        self.button3 = Button(self.menuFrame, text="Highscore", font=("Helvetica", "10", "bold"), width=13, height=2,
                              command=board.show_high_score, relief=RIDGE,)
        self.button3.pack()
        self.button4 = Button(self.menuFrame, text="Exit", font=("Helvetica", "10", "bold"), width=13, height=2,
                              command=board.game_exit, cursor="pirate", relief=RIDGE,)
        self.button4.pack()

        self.settingsFrame = Frame(width=220, height=100)

        self.labelNames1 = Label(self.settingsFrame, text="Player Names", font="bold", relief=RIDGE)
        self.labelNames1.grid(row=0, column=1, sticky=W)
        self.labelNames2 = Label(self.settingsFrame, text="Player 1", font="bold")
        self.labelNames2.grid(row=1, column=0, sticky=W)
        self.labelNames3 = Label(self.settingsFrame, text="Player 2", font="bold")
        self.labelNames3.grid(row=2, column=0, sticky=W)
        self.nameEntry1 = Entry(self.settingsFrame, width=12)
        self.nameEntry1.grid(row=1, column=1, sticky=W)
        self.nameEntry1.rowconfigure(1, pad=2)
        self.nameEntry2 = Entry(self.settingsFrame, width=12)
        self.nameEntry2.grid(row=2, column=1, sticky=W)
        self.nameEntry1.rowconfigure(2, pad=2)

        self.settingsFrame.pack_forget()

        self.mode = IntVar()

        self.labelMode = Label(self.settingsFrame, text="Game Mode", font="bold", relief=RIDGE)
        self.labelMode.grid(row=5, column=1, sticky=W)
        self.radioButtonMode1 = Radiobutton(self.settingsFrame, text="Player vs Player", variable=self.mode, value=1)
        self.radioButtonMode1.grid(row=6, column=1, sticky=W)
        self.radioButtonMode2 = Radiobutton(self.settingsFrame, text="Player vs AI", variable=self.mode, value=2)
        self.radioButtonMode2.grid(row=7, column=1, sticky=W)

        self.board_size_ = IntVar()

        self.labelSize = Label(self.settingsFrame, text="Board Size", font="bold", relief=RIDGE)
        self.labelSize.grid(row=9, column=1, sticky=W)
        self.radioButtonSize1 = Radiobutton(self.settingsFrame, text="8x8", variable=self.board_size_, value=8)
        self.radioButtonSize1.grid(row=10, column=1, sticky=W)
        self.radioButtonSize2 = Radiobutton(self.settingsFrame, text="10x10", variable=self.board_size_, value=10)
        self.radioButtonSize2.grid(row=11, column=1, sticky=W)

        self.piece_color = IntVar()

        self.labelColor = Label(self.settingsFrame, text="Piece Color", font="bold", relief=RIDGE)
        self.labelColor.grid(row=12, column=1, sticky=W)
        self.radioButtonColor1 = Radiobutton(self.settingsFrame, text="Red and Black",
                                             variable=self.piece_color, value=1)
        self.radioButtonColor1.grid(row=13, column=1, sticky=W)
        self.radioButtonColor2 = Radiobutton(self.settingsFrame, text="Gray and Black",
                                             variable=self.piece_color, value=2)
        self.radioButtonColor2.grid(row=14, column=1, sticky=W)
        self.radioButtonColor3 = Radiobutton(self.settingsFrame, text="White and Black",
                                             variable=self.piece_color, value=3)
        self.radioButtonColor3.grid(row=15, column=1, sticky=W)
        self.radioButtonColor4 = Radiobutton(self.settingsFrame, text="Turquoise and Green",
                                             variable=self.piece_color, value=4)
        self.radioButtonColor4.grid(row=16, column=1, sticky=W)


class Board(Tk):
    ''' A class for creating the board, the high score box and the instructions text box and their associated methods.
    '''

    def __init__(self, width=700, height=700, cell_size=70):
        Tk.__init__(self)
        self.cell_size = cell_size
        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.pack(expand=1, side=RIGHT)

        self.textFrame = Frame(width=200, height=20)
        self.textFrame.pack(expand=1, fill=BOTH, side=RIGHT)
        self.textForUser = Text(self.textFrame, width=20, height=4, bg="bisque", font=("verdana", "10"), wrap=WORD)
        self.textForUser.pack()
        self.textForUser.insert(END, "Welcome to checkers!")
        self.textForUser.config(state=DISABLED)

        self.highScoreText = Text(self.textFrame, width=20, height=30, bg="bisque", font=("verdana", "10"), wrap=WORD)

        self.player1_name = "Player 1"
        self.player2_name = "Player 2"

        self.color1 = "red"
        self.color2 = "black"
        self.board_size = 8
        self.empty_rows = 3

        # Used to store each canvas oval
        self.piece_on_board = []

        # The piece that is currently highlighted will be in this list
        self.highlighted_piece_on_board = []

        # Stores the reference variables for the king pieces pictures
        self.reference_dict = {}

        # This variable is assigned to 1 if the mode is player vs player and if it's player vs AI then it's 2
        self.mode = 1

        # Which player turn it is
        self.current_player = 1

        # Gets assigned to the current time when the game starts
        self.start_time = 0

        # Gets assignet to the current time when the game ends
        self.end_time = 0

        # If the game is over it will be set to True
        self.game_over = False

    def delete_text(self):
        '''Empties the instructions text box.

        :return: (nothing)
        '''

        self.textForUser.config(state=NORMAL)
        self.textForUser.delete(0.0, END)
        return

    def enter_text_for_user(self, text):
        '''Enters a text in the instructions text box.

        :param text: The text that should be printed in the text box
        :return: (nothing)
        '''

        self.textForUser.insert(END, text)
        self.textForUser.config(state=DISABLED)
        return

    def start_game(self):
        '''Starts the game and uses the current settings or the default if the user did not select anything.

        :return: (nothing)
        '''

        if menu.mode.get() == 1 or menu.mode.get() == 2:
            self.mode = menu.mode.get()
        if menu.piece_color.get() == 1:
            self.color1 = "red"
            self.color2 = "black"
        elif menu.piece_color.get() == 2:
            self.color1 = "gray67"
            self.color2 = "black"
        elif menu.piece_color.get() == 3:
            self.color1 = "white smoke"
            self.color2 = "black"
        elif menu.piece_color.get() == 4:
            self.color1 = "turquoise1"
            self.color2 = "SeaGreen3"
        if menu.board_size_.get() == 8 or menu.board_size_.get() == 10:
            self.board_size = menu.board_size_.get()
            PlainPiece.board_size_list[0] = menu.board_size_.get()
        self.empty_rows = 4 if menu.board_size_.get() == 10 else 3
        self.canvas.delete("all")
        self.print_start_board()
        self.current_player = 1
        self.delete_text()
        self.player_turn_text()
        self.start_time = time()
        return

    def show_settings(self):
        '''Shows and hides the settings options.

        :return: (nothing)
        '''

        if menu.settingsFrame.winfo_ismapped():
            menu.settingsFrame.pack_forget()
        else:
            menu.settingsFrame.pack(expand=1, fill=BOTH, side=BOTTOM)
            menu.settingsFrame.pack_propagate(0)
        return

    def view_high_score(self):
        '''Writes the high score list into the text box.

        :return: (nothing)
        '''

        time_list_8 = []
        time_list_10 = []

        with open('Highscore.txt', 'r') as f:
            score_list = [line.split(' ') for line in f.read().splitlines()]
            if len(score_list) > 0:
                for lists in score_list:
                    if lists[1] == "8x8":
                        time_list_8.append([lists[2], lists[0], lists[1]])
                    elif lists[1] == "10x10":
                        time_list_10.append([lists[2], lists[0], lists[1]])
                        
        if len(score_list) > 0:
            time_list_8.sort()
            # Only keeps the 10 best times
            time_list_8 = time_list_8[:10]
            time_list_10.sort()
            time_list_10 = time_list_10[:10]

            self.highScoreText.config(state=NORMAL)
            self.highScoreText.delete(0.0, END)
            self.highScoreText.insert(END, "8x8\n", "e")
            self.highScoreText.tag_configure("e", underline=1)

            for times in range(len(time_list_8)):
                # Converts seconds into minutes and seconds
                m, s = divmod(int(time_list_8[times][0]), 60)
                if time_list_8[times][2] == "8x8":
                    self.highScoreText.insert(END, "%d min %02d s  " % (m, s) + " " + time_list_8[times][1] + "\n")

            self.highScoreText.insert(END, "\n10x10\n", "e")
            self.highScoreText.tag_configure("e", underline=1)
            for times in range(len(time_list_10)):
                m, s = divmod(int(time_list_10[times][0]), 60)
                if time_list_10[times][2] == "10x10":
                    self.highScoreText.insert(END, "%d min %02d s  " % (m, s) + " " + time_list_10[times][1] + "\n")

        self.highScoreText.config(state=DISABLED)
        return

    def show_high_score(self):
        '''Shows and hides the high score text box.

        :return: (nothing)
        '''

        self.view_high_score()
        if self.highScoreText.winfo_ismapped():
            self.highScoreText.pack_forget()
        else:
            self.highScoreText.pack()
        return

    def player_turn_text(self):
        '''Writes which player turn it is to move.

        :return: (nothing)
        '''

        self.delete_text()
        if self.current_player == 1:
            if self.mode == 1 or self.mode == 2:
                if menu.nameEntry1.index("end") != 0:
                    self.player1_name = menu.nameEntry1.get()
                    if self.player1_name[-1] == "s":
                        self.enter_text_for_user("It is " + str(self.player1_name) + "' turn to move")
                    else:
                        self.enter_text_for_user("It is " + str(self.player1_name) + "'s turn to move")
                else:
                    self.enter_text_for_user("It is " + str(self.player1_name) + "'s turn to move")

        else:
            if self.mode == 1 or self.mode == 3:
                if len(menu.nameEntry2.get()) != 0:
                    self.player2_name = menu.nameEntry2.get()
                    if self.player2_name[-1] == "s":
                        self.enter_text_for_user("It is " + str(self.player2_name) + "' turn to move")
                    else:
                        self.enter_text_for_user("It is " + str(self.player2_name) + "'s turn to move")
                else:
                    self.enter_text_for_user("It is " + str(self.player2_name) + "'s turn to move")
        return

    def game_exit(self):
        '''Closes the game window.

        :return: (nothing)
        '''

        board.destroy()
        return

    def clean_up_images(self):
        '''Cleans up the reference variables for each image that is not on the board.

        :return: (nothing)
        '''

        images_still_on_board = board.image_names()
        for name in set(self.reference_dict.keys()):
            if name not in images_still_on_board:
                del self.reference_dict[name]
        return

    def on_click(self, event):
        '''Figures out which piece the user has clicked on.

        :return: (nothing)
        '''

        x = int(event.x / self.cell_size)
        y = int(event.y / self.cell_size)
        try:
            self.sort_highlighted_piece(x, y)
        except TypeError as error:
            self.delete_text()
            self.enter_text_for_user(error)
            # The text disappears after 2.1 seconds
            self.textForUser.after(2100, self.delete_text)

    def on_click_square(self, event):
        ''' Figures out which square the user clicked on.

        :return: (nothing)
        '''

        try:
            self.player_turn(event)
        except EnvironmentError as error:
            self.delete_text()
            self.enter_text_for_user(error)
            self.textForUser.after(2100, self.delete_text)
        except TypeError as error:
            self.delete_text()
            self.enter_text_for_user(error)
            self.textForUser.after(2100, self.delete_text)
        except ValueError as error:
            self.delete_text()
            self.enter_text_for_user(error)
            self.textForUser.after(2100, self.delete_text)
        return

    def highlight_piece(self, x, y):
        '''Highlights the piece that is clicked on and adds it to the list.

        :param x: The x-coordinate of the click
        :param y: The y-coordinate of the click
        :return: (nothing)
        '''

        # Assigns the ID of the clicked piece to a variable
        piece_ID = self.get_piece_ID(x, y)

        # Red and black kings have special pictures in game
        red_king = PhotoImage(file="red_king_high.gif")
        black_king = PhotoImage(file="black_king_high.gif")

        if self.color1 == "red" and self.color2 == "black":
            if [x, y] in PlainPiece.pieces_dict[self.current_player]:
                self.reset_highlighted_piece()
                self.canvas.itemconfig(piece_ID, outline="yellow")
                self.highlighted_piece_on_board.append((piece_ID, x, y))

            elif [x, y] in PlainPiece.king_pieces_dict[self.current_player]:
                self.reset_highlighted_piece()
                if self.current_player == 1:
                    self.canvas.itemconfig(piece_ID, image=red_king)
                    self.reference_dict[piece_ID] = red_king
                elif self.current_player == 2:
                    self.canvas.itemconfig(piece_ID, image=black_king)
                    self.reference_dict[piece_ID] = black_king
                self.highlighted_piece_on_board.append((piece_ID, x, y))
            else:
                raise TypeError("You must select a piece of your own!")
        else:
            if [x, y] in PlainPiece.pieces_dict[self.current_player] \
                    or [x, y] in PlainPiece.king_pieces_dict[self.current_player]:
                self.reset_highlighted_piece()
                self.canvas.itemconfig(piece_ID, outline="yellow")
                self.highlighted_piece_on_board.append((piece_ID, x, y))
            else:
                raise TypeError("You must select a piece of your own!")
        return

    def highlight_jump_piece(self):
        '''Highlights the piece that can make another jump move.

        :return: (nothing)
        '''

        piece_ID = self.get_piece_ID(PlainPiece.jump_again_list[0][0], PlainPiece.jump_again_list[0][1])
        red_king = PhotoImage(file="red_king_high.gif")
        black_king = PhotoImage(file="black_king_high.gif")

        # If the piece colors are red and black the king has a special picture
        if self.color1 == "red" and self.color2 == "black":
            if [PlainPiece.jump_again_list[0][0], PlainPiece.jump_again_list[0][1]] \
                    in PlainPiece.king_pieces_dict[self.current_player]:
                self.reset_highlighted_piece()
                if self.current_player == 1:
                    self.canvas.itemconfig(piece_ID, image=red_king)
                    self.canvas.photo1 = red_king
                elif self.current_player == 2:
                    self.canvas.itemconfig(piece_ID, image=black_king)
                    self.canvas.photo2 = black_king
            elif [PlainPiece.jump_again_list[0][0], PlainPiece.jump_again_list[0][1]] \
                    in PlainPiece.pieces_dict[self.current_player]:
                self.reset_highlighted_piece()
                self.canvas.itemconfig(piece_ID, outline="yellow")
        else:
            if [PlainPiece.jump_again_list[0][0], PlainPiece.jump_again_list[0][1]] \
                    in PlainPiece.pieces_dict[self.current_player] or \
                    [PlainPiece.jump_again_list[0][0], PlainPiece.jump_again_list[0][1]] \
                    in PlainPiece.king_pieces_dict[self.current_player]:
                self.reset_highlighted_piece()
                self.canvas.itemconfig(piece_ID, outline="yellow")
        self.highlighted_piece_on_board.append((piece_ID, PlainPiece.jump_again_list[0][0],
                                                PlainPiece.jump_again_list[0][1]))
        return

    def sort_highlighted_piece(self, x, y):
        '''Figures out which piece to highlight.

        :param x: The x-coordinate of the click
        :param y: The y-coordinate of the click
        :return: (nohting)
        '''

        # If a piece can jump again only that piece will be highlighted
        if PlainPiece.jump_again_list:
            self.highlight_jump_piece()
        else:
            if self.highlighted_piece_on_board:
                if [x, y] == [self.highlighted_piece_on_board[0][1], self.highlighted_piece_on_board[0][2]]:
                    self.reset_highlighted_piece()
                    return
            self.highlight_piece(x, y)
        return

    def reset_highlighted_piece(self):
        '''Removes the highlight from the current highlighted piece.

        :return: (nothing)
        '''

        red_king = PhotoImage(file="red_king_piece.gif")
        black_king = PhotoImage(file="black_king_piece.gif")

        if self.highlighted_piece_on_board:
            piece_ID = self.highlighted_piece_on_board[0][0]
            if self.color1 == "red" and self.color2 == "black":
                if [self.highlighted_piece_on_board[0][1], self.highlighted_piece_on_board[0][2]] \
                        in PlainPiece.pieces_dict[self.current_player]:
                    self.canvas.itemconfig(piece_ID, outline="black")
                    # If the color piece is red or black and a king it will change to a normal picture without highlight
                elif [self.highlighted_piece_on_board[0][1], self.highlighted_piece_on_board[0][2]] \
                        in PlainPiece.king_pieces_dict[self.current_player]:
                    if self.current_player == 1:
                        self.canvas.itemconfig(piece_ID, image=red_king)
                        self.reference_dict[piece_ID] = red_king
                    elif self.current_player == 2:
                        self.canvas.itemconfig(piece_ID, image=black_king)
                        self.reference_dict[piece_ID] = black_king
            else:
                if [self.highlighted_piece_on_board[0][1], self.highlighted_piece_on_board[0][2]] \
                        in PlainPiece.pieces_dict[self.current_player] or \
                        [self.highlighted_piece_on_board[0][1], self.highlighted_piece_on_board[0][2]]\
                        in PlainPiece.king_pieces_dict[self.current_player]:
                    self.canvas.itemconfig(piece_ID, outline="black")
            self.highlighted_piece_on_board.clear()
        return

    def get_piece_ID(self, x, y):
        '''Used to get the id of a canvas oval.

        :param x: The current x-coordinate
        :param y: The current y-coordinate
        :return: (nothing)
        '''

        for i in range(len(self.piece_on_board)):
            if x == self.piece_on_board[i][1] and y == self.piece_on_board[i][2]:
                return self.piece_on_board[i][0]

        return 0

    def player_turn(self, event):
        '''If a piece is highlighted it will try to move it to the square that was clicked on.

        :return: (nothing)
        '''

        x = int(event.x / self.cell_size)
        y = int(event.y / self.cell_size)
        if self.highlighted_piece_on_board:
            # Checks if there are any legal jump moves
            check_jump_moves(self.current_player)
            if [self.highlighted_piece_on_board[0][1], self.highlighted_piece_on_board[0][2]] \
                    in PlainPiece.pieces_dict[self.current_player]:
                piece = PlainPiece(self.highlighted_piece_on_board[0][1], self.highlighted_piece_on_board[0][2],
                                   self.current_player)
            elif [self.highlighted_piece_on_board[0][1], self.highlighted_piece_on_board[0][2]] in \
                    PlainPiece.king_pieces_dict[self.current_player]:
                piece = KingPiece(self.highlighted_piece_on_board[0][1], self.highlighted_piece_on_board[0][2],
                                  self.current_player)
            self.reset_highlighted_piece()
            piece.move_piece(x, y)
            self.print_current_board()
            if not PlainPiece.jump_again_list:
                self.switch_player_turn()
                self.delete_text()
                self.player_turn_text()
                if self.check_game_over():
                    return
            else:
                return
            if self.mode == 2:
                self.move_AI()
        return

    def move_AI(self):
        '''Moves a piece for the AI.

        :return: (nothing)
        '''

        board.update()
        sleep(0.7)
        AI_move_piece_on_board(self.current_player)
        self.print_current_board()
        while PlainPiece.jump_again_list:
            board.update()
            sleep(0.7)
            AI_move_piece_on_board(self.current_player)
            self.print_current_board()
        self.switch_player_turn()
        self.delete_text()
        self.player_turn_text()
        self.check_game_over()
        return

    def switch_player_turn(self):
        '''Switches the player turn.

        :return: (nothing)
        '''

        if self.current_player == 1:
            self.current_player = 2
        elif self.current_player == 2:
            self.current_player = 1
        return

    def check_game_over(self):
        '''Checks if the game is over and prints the result in the text box.
        :return: (nothing)
        '''

        if len(PlainPiece.pieces_dict[1]) + len(PlainPiece.king_pieces_dict[1]) == 1 \
                and len(PlainPiece.pieces_dict[2]) + len(PlainPiece.king_pieces_dict[2]) == 1:
            self.delete_text()
            self.enter_text_for_user("It's a draw!")
            self.game_over = True
            self.print_current_board()
            return True
        elif no_valid_moves(self.current_player):
            self.delete_text()
            if self.current_player == 1 and self.mode == 2:
                self.enter_text_for_user("Too bad:(... \nAI wins!!")
            elif self.current_player == 1 and self.mode == 1:
                self.end_time = time()
                add_high_score(self.player2_name, self.board_size, self.start_time, self.end_time)
                self.enter_text_for_user("Congratulations!\n" + self.player2_name + " wins!")
            elif self.current_player == 2 and (self.mode == 1 or self.mode == 2):
                self.end_time = time()
                add_high_score(self.player1_name, self.board_size, self.start_time, self.end_time)
                self.enter_text_for_user("Congratulations!\n" + self.player1_name + " wins!")
            self.game_over = True
            self.print_current_board()
            return True
        return False

    def print_starting_pieces_2(self):
        '''Prints the starting pieces for player 1.

        :return: (nohting)
        '''

        for row in range(self.empty_rows):
            for column in range(self.board_size):
                x1 = (column * self.cell_size)
                y1 = (row * self.cell_size)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if row % 2 == 0:
                    if column % 2 != 0:
                        piece = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color2, outline="black")
                        self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)
                        # Appends the ID of the piece along with their coordinates in a tuple to a list
                        self.piece_on_board.append((piece, column, row))
                        new_piece = [column, row]
                        PlainPiece.pieces_dict[2].append(new_piece)

                elif row % 2 != 0:

                    if column % 2 == 0:
                        piece = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color2, outline="black")
                        self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)
                        self.piece_on_board.append((piece, column, row))
                        new_piece = [column, row]
                        PlainPiece.pieces_dict[2].append(new_piece)
        return

    def print_starting_pieces_1(self):
        '''Prints the starting pieces for player 2.

        :return: (nothing)
        '''

        for row in range(self.board_size - self.empty_rows, self.board_size):
            for column in range(self.board_size):
                x1 = (column * self.cell_size)
                y1 = (row * self.cell_size)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if row % 2 == 0:
                    if column % 2 != 0:
                        piece = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color1, outline="black")
                        self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)
                        self.piece_on_board.append((piece, column, row))
                        new_piece = [column, row]
                        PlainPiece.pieces_dict[1].append(new_piece)
                elif row % 2 != 0:

                    if column % 2 == 0:
                        piece = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color1, outline="black")
                        self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)
                        self.piece_on_board.append((piece, column, row))
                        new_piece = [column, row]
                        PlainPiece.pieces_dict[1].append(new_piece)
        return

    def print_start_board(self):
        '''Prints the starting board.

        :return: (nothing)
        '''

        self.game_over = False
        self.piece_on_board.clear()
        clear_dictionaries()
        self.print_background_board()

        self.print_starting_pieces_2()
        self.print_starting_pieces_1()
        return

    def print_background_board(self):
        '''Prints the background board.

        :return: (nothing)
        '''

        self.canvas.delete("all")
        for (i, j) in product(range(self.board_size), range(self.board_size)):
            x1 = (i * self.cell_size)
            y1 = (j * self.cell_size)
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            color = "bisque" if i % 2 == j % 2 else "burlywood4"
            squares = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="bisque4")
            self.canvas.tag_bind(squares, "<ButtonPress-1>", self.on_click_square)
        return

    def print_current_board(self):
        '''Prints the current board using the dictionaries.

        :return: (nothing)
        '''

        self.clean_up_images()
        self.canvas.delete("all")
        self.piece_on_board.clear()
        self.print_background_board()

        # If the game is over it will print the current board without any binds
        if self.game_over:
            self.print_board_when_finished()
        else:
            self.print_plain_pieces()
            self.print_king_pieces()
        return

    def print_plain_pieces(self):
        '''Prints the current plain pieces from the pieces dictionary.

        :return: (nothing)
        '''

        for player in PlainPiece.pieces_dict:
            for coordinate in PlainPiece.pieces_dict[player]:
                x1 = (coordinate[0] * self.cell_size)
                y1 = (coordinate[1] * self.cell_size)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if player == 1:
                    piece = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color1, outline="black")
                    self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)
                    self.piece_on_board.append((piece, coordinate[0], coordinate[1]))
                elif player == 2:
                    piece = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color2, outline="black")
                    self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)
                    self.piece_on_board.append((piece, coordinate[0], coordinate[1]))
        return

    def print_king_pieces(self):
        '''Prints the current king pieces from the king pieces dictionary.

        :return: (nothing)
        '''

        red_king = PhotoImage(file="red_king_piece.gif")
        black_king = PhotoImage(file="black_king_piece.gif")

        for player in PlainPiece.king_pieces_dict:
            for coordinate in PlainPiece.king_pieces_dict[player]:
                x1 = (coordinate[0] * self.cell_size)
                y1 = (coordinate[1] * self.cell_size)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if player == 1:
                    # If the selected color is red and black a the kings has a special picture
                    if self.color1 == "red" and self.color2 == "black":
                        piece = self.canvas.create_image(x1, y1, image=red_king, anchor=NW)
                        self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)

                        self.reference_dict[piece] = red_king
                        self.piece_on_board.append((piece, coordinate[0], coordinate[1]))
                    else:
                        piece = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color1, outline="black")
                        self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)
                        self.piece_on_board.append((piece, coordinate[0], coordinate[1]))
                elif player == 2:
                    if self.color1 == "red" and self.color2 == "black":
                        piece = self.canvas.create_image(x1, y1, image=black_king, anchor=NW)
                        self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)

                        self.reference_dict[piece] = black_king
                        self.piece_on_board.append((piece, coordinate[0], coordinate[1]))
                    else:
                        piece = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color2, outline="black")
                        self.canvas.tag_bind(piece, "<ButtonPress-1>", self.on_click)
                        self.piece_on_board.append((piece, coordinate[0], coordinate[1]))
        return

    def print_board_when_finished(self):
        '''When the game is over it will print the current board without any binds.

        :return: (nothing)
        '''

        red_king = PhotoImage(file="red_king_piece.gif")
        black_king = PhotoImage(file="black_king_piece.gif")

        for player in PlainPiece.pieces_dict:
            for coordinate in PlainPiece.pieces_dict[player]:
                x1 = (coordinate[0] * self.cell_size)
                y1 = (coordinate[1] * self.cell_size)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if player == 1:
                    self.canvas.create_oval(x1, y1, x2, y2, fill=self.color1, outline="black")
                elif player == 2:
                    self.canvas.create_oval(x1, y1, x2, y2, fill=self.color2, outline="black")
        for player in PlainPiece.king_pieces_dict:
            for coordinate in PlainPiece.king_pieces_dict[player]:
                x1 = (coordinate[0] * self.cell_size)
                y1 = (coordinate[1] * self.cell_size)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if player == 1:
                    if self.color1 == "red" and self.color2 == "black":
                        self.canvas.create_image(x1, y1, image=red_king, anchor=NW)
                        self.canvas.photo = red_king
                    else:
                        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color1, outline="black")
                elif player == 2:
                    if self.color1 == "red" and self.color2 == "black":
                        self.canvas.create_image(x1, y1, image=black_king, anchor=NW)
                        self.canvas.photo = black_king
                    else:
                        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color2, outline="black")


board = Board()
board.title("Checkers")
board.resizable(False, False)
menu = Menu()
board.print_background_board()
board.print_start_board()
menu.mainloop()
board.mainloop()
