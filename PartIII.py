# state is denoted by a dictionary
# use alpha-beta search algorithm

import copy
from itertools import combinations

class states(object):
    def __init__(self):
        self.board = [{'player':[],'comp':[],'left':[1,2,3,4,5,6,7,8,9]}\
         for _ in range(9)]
        self.turn = 1 # if it's computer's turn then turn = 1, else turn = -1
        self.order = 1  # if player choose 'o', then order = 1, else order = -1
        self.last_move = None
        self.global_state = {'player':[], 'comp':[], 'draw':[],\
         'left':[1,2,3,4,5,6,7,8,9]}


class ultimate_tic_tac_toe(object):
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

    def ask_board(self,state):
        while True:
            try:
                board = int(input("Please select a board from {}: "\
                .format(state.global_state['left'])))
            except:
                print("Input error! Please input a number from {}: "\
                .format(state.global_state['left']))
                continue
            if not board in state.global_state['left']:
                print("Input error! Please input a number from {}: "\
                .format(state.global_state['left']))
                continue
            break
        return board

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

        global_res = ['-' for _ in range(9)]
        for j in state.global_state['player']:
            global_res[j-1] = 'o' if state.order == 1 else 'x'
        for j in state.global_state['comp']:
            global_res[j-1] = 'x' if state.order == 1 else 'o'
        for j in state.global_state['draw']:
            global_res[j-1] = '*'
        print('Here is the current global state:')
        for i in range(3):
            print('  {} {} {}'.format(global_res[3*i], global_res[3*i+1],\
            global_res[3*i+2]))

        if state.turn>0:
            print("\nIt's computer's turn.")
        else:
            print("\nIt's your turn.")

        print("  -----------------------------------------------------------")

    def check_board(self, board):
        win_state = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]
        for i in win_state:
            if i.issubset(board['comp']):
                return 1
            elif i.issubset(board['player']):
                return -1
        if len(board['left']) == 0:
            return 0
        return None

    def change_state(self, state, board, move):
        s = copy.deepcopy(state)
        s.board[board-1]['left'].remove(move)
        if s.turn>0:
            s.board[board-1]['comp'].append(move)
        else:
            s.board[board-1]['player'].append(move)
        s.turn *= -1
        s.last_move = move
        v = self.check_board(s.board[board-1])
        if v != None:
            s.global_state['left'].remove(board)
            if v == 1:
                s.global_state['comp'].append(board)
            elif v == -1:
                s.global_state['player'].append(board)
            else:
                s.global_state['draw'].append(board)
        return s

    def action_search(self, state):
        assert state.turn == 1
        if self.check_board(state.global_state) != None:
            return (None,None)
        val = float('-inf')
        b, a = (None, None)
        board = state.last_move
        for i in state.global_state['left']:
            if board in state.global_state['left'] and i != board:
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
        v = self.check_board(state.global_state)
        if v != None:
            return v
        if d == 3:
            return self.eval(state)
        v = float('-inf')
        board = state.last_move
        for i in state.global_state['left']:
            if board in state.global_state['left'] and i != board:
                continue
            for j in state.board[i-1]['left']:
                new_state = self.change_state(state, i, j)
                val = self.Min_Value(new_state, mini, maxi, d+1)
                v  = max(v,val)
                if v >= maxi:
                        return v
                mini = max(mini,v)
        return v

    def Min_Value(self, state, mini, maxi, d):
        v = self.check_board(state.global_state)
        if v != None:
            return v
        v = float('inf')
        board = state.last_move
        for i in state.global_state['left']:
            if board in state.global_state['left'] and i != board:
                continue
            for j in state.board[i-1]['left']:
                new_state = self.change_state(state, i, j)
                val = self.Max_Value(new_state, mini, maxi, d+1)
                v = min(v,val)
                if v <= mini:
                    return v
            maxi = min(maxi,v)
        return v

    def eval(self, state):
        assert state.turn == 1
        finishing_boards = {'player':[], 'comp':[]}
        for board in state.global_state['left']:
            temp = self.check_finishing(state.board[board-1])
            if temp[0] == 1:
                finishing_boards['comp'].append(board)
            if temp[1] == 1:
                finishing_boards['player'].append(board)
        # player_finishing and comp_finishing are number of borads that the player
        # and the computer is one step from the win.
        player_finishing = len(finishing_boards['player'])
        comp_finishing = len(finishing_boards['comp'])
        # player_finished and comp_finished are number of boards that the player
        # and the computer have won.
        player_finished = len(state.global_state['player'])
        comp_finished = len(state.global_state['comp'])
        l = len(state.board[state.last_move-1]['left'])
        # c and p is the result of checking whether the computer or the player
        # is one step from the win on the global 3*3 board.
        c, p = self.check_finishing(state.global_state)
        win_state = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]

        # Consider the corner case that computer can play on any board in the
        # next move.
        if not state.last_move in state.global_state['left']:
            for i in win_state:
                for j in finishing_boards['comp']:
                    if i.issubset(state.global_state['comp']+[j]):
                        return 1
            # If teh computer can win in one step, then return 1.
            return ((c-p)*0.5 + (comp_finishing - player_finishing)*0.15 + \
                    (comp_finished - player_finished)*0.2)

        # Consider general cases that computer can only play on the
        # corresponding board of the last move.
        # If the computer can win in one step, then return 1.
        else:
            if state.last_move in finishing_boards['comp']:
                for i in win_state:
                    if i.issubset(state.global_state['comp']+[state.last_move]):
                        return 1
            # If the computer cannot directly win, then divide the possible moves
            # into four gourps.
            dead, free, finish, other = 0, 0, 0, 0
            for k in state.board[state.last_move-1]['left']:
                if not k in state.global_state['left']:
                    free += 1
                elif k in finishing_boards['player'] and [i.issubset(state.global_state\
                ['player']+[k]) for i in win_state]:
                    dead += 1
                elif k in finishing_boards['comp']:
                    finish += 1
                else:
                    other += 1
            # Give each group a coefficient and calculate the weighted average.
            other_effi = (comp_finishing - player_finishing)*0.15 + \
                        (comp_finished*0.3 - player_finished*0.1)
            free_effi = p*(-0.7) + (comp_finishing - player_finishing)*0.15 + \
                        (comp_finished*0.3 - player_finished*0.1) - 0.5
            finish_effi = (comp_finishing - player_finishing)*0.15 + \
                        ((comp_finished+1) *0.3- player_finished*0.1)
            score = ((-1)*dead + free_effi*free + finish_effi*finish + \
                    other_effi*other)/l
            return score

    def check_finishing(self, board):
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
        return (c, p)

    def action_ask(self, state):
        assert state.turn == -1
        if self.check_board(state.global_state) != None:
            return (None, None)
        board = state.last_move
        if not board in state.global_state['left']:
            print("You cannot play on board No.{}, please select another board."\
            .format(board))
            board = self.ask_board(state)
            state.last_move = board
        move = self.ask_move(state)
        return (board,move)

    def print_result(self, state):
        res = self.check_board(state.global_state)
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


game1 = ultimate_tic_tac_toe()
game1.implement()
