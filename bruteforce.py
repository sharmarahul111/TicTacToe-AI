# 1 => favours first turn
# -1 => favours second turn

unique_boards = set()
dataset = {}
root_node = ((0,0,0),(0,0,0),(0,0,0))
# root_node = ((1,-1,1),(1,0,0),(0,0,0))
root_node = ((-1,1,-1),(0,1,0),(0,-1,1))
print(f"[INFO] Starting with root node: {root_node}")
search_list = [root_node]
# returns 0 if game isn't over
def check_end(tup):
	for i in range(3):
		# row
		if tup[i][0] and (tup[i][0] == tup[i][1] == tup[i][2]):
			return tup[i][0]
		# col
		if tup[0][i] and (tup[0][i] == tup[1][i] == tup[2][i]):
			return tup[0][i]

	# diagonal
	if tup[0][0] and tup[0][0] == tup[1][1] == tup[2][2]:
		return tup[1][1]
	if tup[0][2] and tup[0][2] == tup[1][1] == tup[2][0]:
		return tup[1][1]
	
	# check if board is filled
	for row in tup:
		for cell in row:
			if cell==0: return 0
	
	return "draw"

def get_player(board):
	count = 0
	for row in board:
		for cell in row:
			if cell != 0:
				count += 1

	return 1 if count % 2 == 0 else -1

def get_legal_moves(tup) -> list[tuple]:
	if check_end(tup):
		return []
	moves = []
	for i in range(3):
		for j in range(3):
			if tup[i][j] == 0:
				moves.append((i,j))
	return moves

def play(tup):
	legal_moves = get_legal_moves(tup)
	board_positions = []
	# convert to list for alteration
	lst = [list(l) for l in tup]
	player = get_player(tup)
	for (i,j) in legal_moves:
		lst[i][j] = player
		board_positions.append(tuple([tuple(l) for l in lst]))
		lst[i][j] = 0
	return board_positions


# score = [win, draw, loss] for first player as 1
def get_score(code):
	if code == 1: return "win"
	elif code == "draw": return "draw"
	elif code == -1: return "loss"
	else:
		print(code)
		raise "Unknown code"

def classify_board(board):
	if check_end(board):
		dataset[board]["forced"] = get_score(check_end(board))
		return dataset[board]["forced"]
	# return the scores if this position is already evaluated
	if dataset[board]["done"]:
		return dataset[board]["forced"]
	# listify the board from tuple
	board_list = [list(b) for b in board]

	player = get_player(board)
	
	wins = 0
	draws = 0
	losses = 0
	# recursively dig deeper into each legal board positions
	for (i,j) in dataset[board]["legal_moves"]:
		# (i,j) = dataset[board]["legal_moves"].pop()
		board_list[i][j] = player
		tpl = tuple([tuple(l) for l in board_list])
		forced = classify_board(tpl)
		# depending on whose turn is to play, win-loss may differ
		dataset[board]["turn"] = player
		if forced == "loss":
			wins += 1
			dataset[board]["win"].append((i,j))
		elif forced == "draw":
			draws += 1
			dataset[board]["draw"].append((i,j))
		else:
			losses += 1
			dataset[board]["loss"].append((i,j))
		
		board_list[i][j] = 0
	# reset change to board for next iteration
	if wins > 0:
		dataset[board]["forced"] = "win"
	elif draws > 0:
		dataset[board]["forced"] = "draw"
	else:
		dataset[board]["forced"] = "loss"
	dataset[board]["done"] = True
	return dataset[board]["forced"]
	
	

# print(search_list[0])
# print(get_legal_moves(search_list[0]))
# print(check_end(search_list[0]))
# print(play(search_list[0]))


print("[INFO] Exploring every legal moves...")
count = 0
while search_list and count < 2_000_000:
	# moves = get_legal_moves(search_list[-1])
	search_list += play(search_list[0])
	# print(search_list.pop(0))
	unique_boards.add(search_list.pop(0))
	count+=1
print(f"[INFO] {count} nodes were found...")
print(f"[INFO] {len(unique_boards)} unique boards were found...")
print(f"[INFO] Adding unique board positions to dataset...")
for board in unique_boards:
	dataset[board] = {
		"legal_moves": get_legal_moves(board),
		"forced": "",
		# move priority in this order
		"win": [],
		"draw": [],
		"loss": [],
		"turn": 1,
		"done": False
	}
print(f"[INFO] Added to dataset...")
print(f"[INFO] Proceeding to classify [win,draw,loss] cases...")
classify_board(root_node)
print(f"[INFO] Done classifying...")
print(f"[INFO] For current position we have a forced [{ dataset[root_node]['forced']}]")
for d,k in dataset.items():
	print(d, k)