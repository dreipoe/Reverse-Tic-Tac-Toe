from random import randint

N = 10
SIGN_PLAYER, SIGN_BOT = 'x', 'o'
board = ['-' for i in range(N * N)]

def get_cell(x, y):
	return board[N*x + y]

def set_cell(val, x, y):
	board[N*x + y] = val

def choose_sign():
	_sign_player, _sign_bot = SIGN_PLAYER, SIGN_BOT
	sign = input('Выберите, за кого будете играть (x/o) [x]: ').lower()
	if sign == SIGN_BOT:
		_sign_bot = SIGN_PLAYER
		_sign_player = sign
	return _sign_player, _sign_bot

def get_sign(player):
	return SIGN_PLAYER if player else SIGN_BOT

def analyze_move(x):
	y = x % N
	x = x // N
	# считаем кол-во занятых полей в пределах 5 клеток по горизонтали или вертикали
	busy = analyze_horizonal(x, y) + analyze_vertical(x, y)
	return busy

def analyze_horizonal(x, y):
	busy = 0
	a = max(0, y - 4)
	b = min(N, y + 5)
	for i in range(a, b):
		if get_cell(x, i) != '-':
			busy += 1
	return busy

def analyze_vertical(x, y):
	busy = 0
	a = max(0, x - 4)
	b = min(N, x + 5)
	for i in range(a, b):
		if get_cell(i, y) != '-':
			busy += 1
	return busy

def bot_move():
	print('Ход соперника...')

	attempt = 0
	while True:
		x = randint(0, N*N - 1)
		if board[x] == '-':
			# если ИИ долго не может найти подходящее поле, он становится менее требовательным к выбору
			if analyze_move(x) > attempt // 3:
				attempt += 1
			else:
				board[x] = SIGN_BOT
				break

def player_move():
	while True:
		while True:
			s = input("Введите номер ячейки (формат XY, где X - строка, Y - столбец): ")
			if s.isdigit():
				x = int(s)
				break
			else:
				print('Неверный формат')

		if x in range(N * N):
			if board[x] == '-':
				board[x] = SIGN_PLAYER
				break
			else:
				print("Эта ячейка занята, пожалуйста, выберите другую.")
		else:
			print('Неверный формат')

def move(player):
	player_move() if player else bot_move()

def print_field():
	# выводим номера столбцов
	print(' ', end=' ')
	for i in range(N):
		print(i, end=' ')
	print()

	# выводим игровое поле, каждая строка начинается с её номера
	for i in range(N):
		print(i, end=' ')
		for j in range(N):
			print(get_cell(i, j), end=' ')
		print()

def check_win(player):
	if '-' not in board:
		print("Игра закончилась вничью")
		return True

	sign = get_sign(player)
	msg_who_wins = "Соперник выиграл" if player else "Вы выиграли"

	if check_horizontals_and_verticals(sign) or check_diagonals(sign):
		print(msg_who_wins)
		return True
	
	return False

def check_horizontals_and_verticals(sign):
	for i in range(N):
		x_limit = y_limit = 0
		for j in range(N):
			# проходит по каждой клетке игрового поля, пытаясь определить ряды из 5 знаков
			x_limit = 0 if get_cell(i, j) != sign else x_limit + 1
			y_limit = 0 if get_cell(j, i) != sign else y_limit + 1
			if x_limit == 5 or y_limit == 5:
				return True
	return False

def check_diagonals(sign):
	# сначала проходит по главным диагоналям, а затем симметрично сканирует сторонние диагонали, исключая ряды в углах
	for i in range(N - 4):
		x, y1, y2 = i, 0, N - 1
		left_x_limit = left_y_limit = right_x_limit = right_y_limit = 0
		while x < N:
			left_x_limit = 0 if get_cell(x, y1) != sign else left_x_limit + 1
			right_x_limit = 0 if get_cell(x, y2) != sign else right_x_limit + 1
			if x != y1:
				left_y_limit = 0 if get_cell(y1, x) != sign else left_y_limit + 1
				right_y_limit = 0 if get_cell(y2, x) != sign else right_y_limit + 1

			if 5 in (left_x_limit, left_y_limit, right_x_limit, right_y_limit):
				return True
			x += 1
			y1 += 1
			y2 -= 1
	return False

def lets_play_again():
	POSITIVE_ANSWERS = {'д', 'да', 'y', 'yes'}
	NEGATIVE_ANSWERS = {'н', 'нет', 'n', 'no'}
	ANSWERS = POSITIVE_ANSWERS | NEGATIVE_ANSWERS

	while True:
		key = input('Начнёте следующую игру? [д/н]: ')
		result = key in POSITIVE_ANSWERS
		if key in ANSWERS:
			return key in POSITIVE_ANSWERS

if __name__ == "__main__":
	print('Добро пожаловать в игру "Обратные крестики-нолики 10 на 10"')

	play = True
	while play:
		SIGN_PLAYER, SIGN_BOT = choose_sign()
		PLAYER_SWITCH = PLAYER_WALKS_FIRST = bool(randint(0, 1))
		print('Вы ходите первым' if PLAYER_WALKS_FIRST else 'Соперник ходит первым')
		print_field()

		while True:
			move(PLAYER_SWITCH)
			print_field()

			if check_win(PLAYER_SWITCH):
				break

			PLAYER_SWITCH = not PLAYER_SWITCH

		board = ['-' for i in range(N * N)]

		play = lets_play_again()
