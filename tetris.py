from tkinter import *
import random
import time

#global variables

#canvas dimensions
width = 250
height = 500

#starting speed
delay = 1000

#time to level up
level_up = 60000

#time to display messages
message_length = 2000

#base number of points for clearing a line
points = 100

#default font
font = ("Helvetica", "20")


class Tetrimino:
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.shape = shape

	def __len__(self):
		return len(self.shape)

	def drop(self):
		self.y += 1

	def left(self):
		self.x -= 1

	def right(self):
		self.x += 1

	def rotate_left(self):
		new_shape = []
		size = len(self)
		for i in range(0, size):
			new_shape.append([])
		for row in self.shape:
			for j, square in enumerate(row):
				new_shape[size - j - 1].append(square)
		self.shape = new_shape

	def rotate_right(self):
		self.rotate_left()
		self.rotate_left()
		self.rotate_left()

	def draw(self, canvas):
		for i, row in enumerate(self.shape):
			for j, square in enumerate(row):
				if square is not None:
					square.draw(canvas, self.x + j, (self.y - 2) + i)

	def draw_shadow(self, canvas):
		for i, row in enumerate(self.shape):
			for j, square in enumerate(row):
				if square is not None:
					shadow = Shadow_Square(square.color)
					shadow.draw(canvas, self.x + j, (self.y - 2) + i)



class I(Tetrimino):
	def __init__(self):
		square = Square("cyan")
		shape = [[square, None, None, None],
				[square, None, None, None],
				[square, None, None, None],
				[square, None, None, None]]
		super().__init__(4, 0, shape)

class J(Tetrimino):
	def __init__(self):
		square = Square("blue")
		shape = [[square, square, square],
				[None, None, square],
				[None, None, None]]
		super().__init__(3, 0, shape)

class L(Tetrimino):
	def __init__(self):
		square = Square("orange")
		shape = [[square, square, square],
				[square, None, None],
				[None, None, None]]
		super().__init__(3, 0, shape)

class O(Tetrimino):
	def __init__(self):
		square = Square("yellow")
		shape = [[square, square],
				[square, square]]
		super().__init__(4, 0, shape)

class S(Tetrimino):
	def __init__(self):
		square = Square("green")
		shape = [[None, square, square],
				[square, square, None], 
				[None, None, None]]
		super().__init__(3, 0, shape)

class T(Tetrimino):
	def __init__(self):
		square = Square("purple")
		shape = [[square, square, square], 
				[None, square, None],
				[None, None, None]]
		super().__init__(3, 0, shape)

class Z(Tetrimino):
	def __init__(self):
		square = Square("red")
		shape = [[square, square, None],
				[None, square, square],
				[None, None, None]]
		super().__init__(3, 0, shape)

class Square():
	def __init__(self, color):
		self.color = color
		self.size = width / 10

	def draw(self, canvas, x, y):
		canvas.create_rectangle(x * self.size, y * self.size, x * self.size + self.size, 
			y * self.size + self.size, fill=self.color)

class Shadow_Square(): 
	def __init__(self, color):
		self.color = color
		self.size = width / 10 

	def draw(self, canvas, x, y):
		canvas.create_rectangle(x * self.size, y * self.size, x * self.size + self.size, 
			y * self.size + self.size, outline=self.color)

def generate_next_piece():
	x = random.randint(0,6)
	if x == 0:
		return I()
	elif x == 1:
		return J()
	elif x == 2:
		return L()
	elif x == 3:
		return O()
	elif x == 4:
		return S()
	elif x == 5:
		return T()
	elif x ==6:
		return Z()


class GameBoard():
	def __init__(self):
		self.board = [[None, None, None, None, None, None, None, None, None, None], 
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None], 
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None],
					[None, None, None, None, None, None, None, None, None, None]]
		self.piece = generate_next_piece()
		self.shadow = None
		self.width = width
		self.height = height
		self.delay = delay
		self.score = 0
		self.streak = 1
		self.level = 1
		self.message = None
		self.playing = False
		

	def draw(self, canvas):
		if self.playing: 
			canvas.delete("all")
			canvas.create_text((width * .75, height * .1), text=str(self.score), font=font)
			if self.message is not None:
				canvas.create_text((width * .25, height * .1), text=self.message, font=font)
			if self.shadow is not None: 
				self.shadow.draw_shadow(canvas)
			if self.piece is not None:
				self.piece.draw(canvas)
			for i, row in enumerate(self.board):
				for j, square in enumerate(row):
					if square is not None:
						square.draw(canvas, j, i)
		else: 
			display = "Gameover!\nFinal Score: " + str(self.score)
			canvas.create_text((width * .5, height * .5), font=font, text=display)

	def __str__(self):
		s = ""
		for row in self.board:
			for square in row:
				if square is None:
					s += "None "
				else:
					s += str(square.color) + " "
			s += "\n"
		return s


	def __repr__(self):
		return str(self)


def down_collision(board, piece):
	for i, row in enumerate(piece.shape):
		for j, square in enumerate(row):
			if square is not None: 
				if piece.y + i +  1 > 19:
					return True
				if board.board[piece.y + i + 1][piece.x + j] is not None:
					return True
	return False

def wall_collision_decorator(left):
	def inner(board): 
		size = len(board.piece)
		boundary = board.piece.x
		flag = False
		for j in range(0, size): 
			if left: 
				for i in range(0, size):
					if board.piece.shape[j][i] is not None:
						flag = True
						break
			else:
				for i in range(size - 1, -1, -1):
					if board.piece.shape[j][i] is not None:
						flag = True
						break
			if flag:
				break
		boundary += i
		if left: 
			if boundary <= 0: 
				return True
		else: 
			if boundary >= 9:
				return True
		return False
	return inner

wall_collision_left = wall_collision_decorator(True)
wall_collision_right = wall_collision_decorator(False)

board = GameBoard()

def make_shadow():
	shadow = Tetrimino(board.piece.x, board.piece.y, board.piece.shape)
	downs = 0
	while not down_collision(board, shadow):
		downs += 1
		shadow.drop()
	return shadow

def main():
	root = Tk()
	canvas = Canvas(root, width=width, height=height)
	canvas.pack()
	canvas.create_text((width * .5, height * .5), width = width - 10, font=("Helvetica", 12), text="Welcome to Tetris! Press p to play\n\nRules:\nClear as many lines as you can until the tetriminos reach the top of the board (streaks and combos will increase score). Each minute of play you will level up for higher clear values but faster drop times. \n\nControls:\nZ/<Up>: rotate left,\nX: rotate left\n<Left>:move left\n<Right>: move right\n<Down>: force down\n<Space>: auto drop")

	def clear_message():
		print("clearing")
		board.message = None

	def play(event):
		board.playing = not board.playing

	def gameover():
		if not all(segment is None for segment in board.board[0] + board.board[1]):
			board.playing = False
			board.draw(canvas)
	
	def piece_to_board():
		check = set()
		for i, row in enumerate(board.piece.shape):
			for j, square in enumerate(row):
				if square is not None:
					board.board[board.piece.y + i][board.piece.x + j] = square
					check.add(board.piece.y + i)
		gameover()
		if board.playing:
			cleared = 0
			for line in check:
				if all(segment is not None for segment in board.board[line]):
					del board.board[line]
					cleared += 1
					board.board.insert(0, [None, None, None, None, None, None, None, None, None, None])
			if cleared != 0:
				if cleared > 1 and board.streak > 1: 
					board.message = "Combo!"
					canvas.after(message_length, clear_message)
				elif cleared == 2: 
					board.message = "Double!"
					canvas.after(message_length, clear_message)
				elif cleared == 3:
					board.message = "Triple!"
					canvas.after(message_length, clear_message)
				elif cleared == 4:
					board.message = "Quad!"
					canvas.after(message_length, clear_message)
				elif board.streak > 1: 
					board.message = "Streak! x" + str(board.streak)
					canvas.after(message_length, clear_message)
				board.score = board.score + (board.level * cleared * board.streak * points) 
				board.streak += 1
			else:
				board.streak = 1
			board.piece = generate_next_piece()
			board.shadow = make_shadow()

	def full_drop(event):
		if board.playing: 
			while not down_collision(board, board.piece):
				board.piece.drop()
			piece_to_board()
			board.draw(canvas)

	def down():
		if down_collision(board, board.piece):
			piece_to_board()
		else: 
			board.piece.drop()		
		board.draw(canvas)

	def down_event(event):
		if board.playing: 
			down()

	def auto_down(): 
		if board.playing:
			down()
		canvas.after(board.delay, auto_down)

	def speed_up():
		board.delay -= 50
		board.level += 1
		board.message = "LEVEL " + str(board.level) + "!"
		canvas.after(message_length, clear_message)
		canvas.after(level_up, speed_up)

	def left(event):
		if board.playing:
			if not wall_collision_left(board):
				board.piece.left()
				board.shadow = make_shadow()
				board.draw(canvas)

	def right(event):
		if board.playing: 
			if not wall_collision_right(board):
				board.piece.right()
				board.shadow = make_shadow()
				board.draw(canvas)

	def rotate_correct():
		back = False
		while wall_collision_left(board):
			back = True
			board.piece.right()
		if back:
			board.piece.left()
		while wall_collision_right(board):
			back = True
			board.piece.left()
		if back: 
			board.piece.right
		board.shadow = make_shadow()
		board.draw(canvas)

	def rotate_l(event):
		if board.playing: 
			board.piece.rotate_left()
			rotate_correct()

	def rotate_r(event):
		if board.playing: 
			board.piece.rotate_right()
			rotate_correct()

	root.bind("p", play)
	root.bind("z", rotate_l)
	root.bind("x", rotate_r)
	root.bind("<Left>", left)
	root.bind("<Right>", right)
	root.bind("<Up>", rotate_l)
	root.bind("<Down>", down_event)
	root.bind("<space>", full_drop)

	canvas.after(board.delay, auto_down)
	canvas.after(level_up, speed_up)
	mainloop()



if __name__ == "__main__":
    """ Runs main() if we run this file with 'python3 hw1.py'. """
    main()