# state is denoted by a dictionary
# use alpha-beta search algorithm

import copy
from itertools import combinations

class states:
    def __init__(self):
        self.board = [{'player':[],'comp':[],'left':[1,2,3,4,5,6,7,8,9]}\
         for _ in range(9)]
        self.turn = 1 # if it's computer's turn then turn = 1, else turn = -1
        self.order = 1  # if player choose 'o', then order = 1, else order = -1
        self.last_move = None
        self.nonfull = [1,2,3,4,5,6,7,8,9] # indicates the boards that are not yet full.


class tic_tac_toe_9:
    def initialize(self):
        while True:
            order = input("Which player do you want to choose, 'x' or 'o': ")
            order = order.strip().lower()
            if not order in ['x','o']:
                print("Input error! Please input 'x' or 'o': ")
                continue
            break
        if order == 'x':
            state = states()
            state.order = -1
            state.turn = -1
            board = self.ask_board(state)
            state.last_move = board
            move = self.ask_move(state)
            initial_state = self.change_state(state,board,move)
        else:
            state = states()
            state.last_move = 5
            initial_state = self.change_state(state,5,5)
        self.print_state(initial_state)
        return initial_state

    # Ask the player to choose a board.
    def ask_board(self,state):
        while True:
            try:
                board = int(input("Please select a board from {}: ".format(state.nonfull)))
            except:
                print("Input error! Please input a number from {}: ".format(state.nonfull))
                continue
            if not board in state.nonfull:
                print("Input error! Please input a number from {}: ".format(state.nonfull))
                continue
            break
        return board

    # Ask the player to choose a move on the given board.
    def ask_move(self,state):
        board = state.last_move
        left = state.board[board-1]['left']
        while True:
            try:
                move = int(input("Please select a move from board {}, position{}: "\
                .format(board, left)))
            except:
                print("Input error! Please input a number from {}: ".format(left))
                continue
            if not move in left:
                print("Input error! Please input a number from {}".format(left))
                continue
            break
        return move

    def print_state(self, state):
        res = [['-' for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in state.board[i]['player']:
                res[i][j-1] = 'o' if state.order == 1 else 'x'
            for j in state.board[i]['comp']:
                res[i][j-1] = 'x' if state.order == 1 else 'o'
        print('\n  -------------------------')
        for l in range(3):
            for s in range(3):
                print("  {} {} {}  |  {} {} {}  |  {} {} {}".format\
                (res[l*3][s*3],res[l*3][s*3+1],res[l*3][s*3+2],res[l*3+1][s*3],\
                res[l*3+1][s*3+1],res[l*3+1][s*3+2],res[l*3+2][s*3],\
                res[l*3+2][s*3+1],res[l*3+2][s*3+2]))
            print('  -------------------------')

        if state.turn>0:
            print("It's computer's turn.")
        else:
            print("It's your turn.")

    # Check wheter the game is over. If the computer wins, return 1; if the player
    # wins, return -1; if draw, return 0; if the game isn't over, return None.
    def check_state(self, state):
        win_state = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]
        for board in state.board:
            for i in win_state:
                if i.issubset(board['comp']):
                    return 1
                if i.issubset(board['player']):
                    return -1
        if len(state.nonfull) == 0:
            return 0
        return None

    def change_state(self, state, board, move):
        s = copy.deepcopy(state)
        s.board[board-1]['left'].remove(move)
        if len(s.board[board-1]['left']) == 0:
            s.nonfull.remove(board)
        if s.turn>0:
            s.board[board-1]['comp'].append(move)
        else:
            s.board[board-1]['player'].append(move)
        s.turn *= -1
        s.last_move = move
        return s

    def action_search(self, state):
        assert state.turn == 1
        if self.check_state(state) != None:
            return (None,None)
        val = float('-inf')
        b, a = (None, None) # b is the board and a is the action on that board.
        board = state.last_move
        for i in state.nonfull:
            if board in state.nonfull and i != board:
                continue
            for j in state.board[i-1]['left']:
                d = 0
                new_state = self.change_state(state,i,j)
                v = self.Min_Value(new_state,float('-inf'),float('inf'),d)
                if v == 1:
                    return (i,j)
                elif v > val:
                    val = v
                    b, a = i, j
        return (b,a)

    def Max_Value(self, state, mini, maxi, d):
        v = self.check_state(state)
        if v != None:
            return v
        if d == 5:
            return self.eval(state)
        v = float('-inf')
        board = state.last_move
        for i in state.nonfull:
            if board in state.nonfull and i != board:
                continue
            for j in state.board[i-1]['left']:
                new_state = self.change_state(state,i,j)
                val = self.Min_Value(new_state, mini, maxi, d+1)
                v  = max(v,val)
                if v >= maxi:
                    return v
                mini = max(mini,v)
        return v

    def Min_Value(self, state, mini, maxi, d):
        v = self.check_state(state)
        if v != None:
            return v
        v = float('inf')
        board = state.last_move
        for i in state.nonfull:
            if board in state.nonfull and i != board:
                continue
            for j in state.board[i-1]['left']:
                new_state = self.change_state(state,i,j)
                val = self.Max_Value(new_state, mini, maxi, d+1)
                v = min(v,val)
                if v <= mini:
                    return v
                maxi = min(maxi,v)
        return v

    def eval(self, state):
        assert state.turn == 1
        res = dict() # Store the situation of each board that whether the board
                     # is one step from win to the player and the computer
        for board in state.nonfull:
            res[board] = self.check_board(state.board[board-1])
        count_player = 0
        count_comp = 0
        for j in res.values():
            if j[0] == 1: count_comp += 1
            if j[1] == 1: count_player += 1

        if not state.last_move in state.nonfull:
            return 1 if count_comp > 0 else (-1)*count_player/len(state.nonfull)
        else:
            if res[state.last_move][0] == 1:
                return 1
            else:
                death, free, other = 0, 0, 0
                for k in state.board[state.last_move-1]['left']:
                    if not k in state.nonfull:
                        free += 1
                    elif res[k][1] == 1:
                        death += 1
                    else:
                        other += 1
                death_effi = -1
                other_effi = (count_comp - count_player)/len(state.nonfull)
                free_effi = -1 if count_player > 0 else count_comp/len(state.nonfull)
                l = len(state.board[state.last_move-1]['left'])
                return (free*free_effi + death*death_effi + other*other_effi)/l

    # Check whether a given board is one step from a win.
    def check_board(self, board):
        if len(board['left']) in [8,9]:
            return (0,0)
        c, p = 0, 0
        win_state = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]
        for i in win_state:
            if c == 1 and p == 1:
                break
            for j in board['left']:
                if j not in i:
                    continue
                if i.issubset(board['comp']+[j]):
                    c = 1
                if i.issubset(board['player']+[j]):
                    p = 1
        return (c, p) # c and p represent whether the computer and the player
                      # are one step from win respectively.

    def action_ask(self, state):
        assert state.turn == -1
        if self.check_state(state) != None:
            return (None, None)
        board = state.last_move
        if not board in state.nonfull:
            print("The board is full, please select another board.")
            board = self.ask_board(state)
            state.last_move = board
        move = self.ask_move(state)
        return (board,move)

    def print_result(self, state):
        res = self.check_state(state)
        if res == 1:
            print('Computer wins!')
        elif res == -1:
            print('You win!')
        else:
            print('Draw!')

    def implement(self):
        state = self.initialize()
        while True:
            if state.turn == 1:
                b, a = self.action_search(state)
            else:
                b, a = self.action_ask(state)
            if a == None:
                self.print_result(state)
                return
            state = self.change_state(state,b,a)
            self.print_state(state)


game1 = tic_tac_toe_9()
game1.implement()
