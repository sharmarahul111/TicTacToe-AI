# 1 => favours first turn
# -1 => favours second turn
# possible status: unsearched, searching, searched, endgame
dataset = {
	# ((0,0,0),(0,0,0),(0,0,0)): {
	# 	"status": "unsearched",
	# 	"moves": {
	# 		1:[],
	# 		0:[],
	# 		-1:[]
	# 	}
	# }
}
count = 0
# search_list = [((0,0,0),(0,0,0),(0,0,0))]
# search_list = [((-1,0,1),(0,1,0),(-1,0,0))]
search_list = [((0,0,0),(0,0,0),(0,0,0))]
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
	player = 1 # assume first player's turn
	if len(legal_moves) % 2 == 0:
		# second player's turn (1)
		player = -1
	for (i,j) in legal_moves:
		lst[i][j] = player
		board_positions.append(tuple([tuple(l) for l in lst]))
		lst[i][j] = 0
	return board_positions

# print(search_list[0])
# print(get_legal_moves(search_list[0]))
# print(check_end(search_list[0]))
# print(play(search_list[0]))


# exit()
unique_boards = set()
while search_list and count < 2_000_000:
	# moves = get_legal_moves(search_list[-1])
	search_list += play(search_list[0])
	# print(search_list.pop(0))
	unique_boards.add(search_list.pop(0))
	# search_list.pop(0)
	count+=1
	if count % 50000 == 0: print(count)
print(count)
print("Unique boards:", len(unique_boards))
# print(play(search_list[0]))
# for i in play(search_list[0]):
# 	print(i)